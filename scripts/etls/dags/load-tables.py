import glob
import pandas as pd
import numpy as np
import sys
import uuid


from datetime import datetime
from sqlalchemy import exc
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator

from operators.Models.BranchOffice import BranchOffice
from operators.Models.BranchOffice import HistBranchOffice
from operators.Models.Car import Car
from operators.Models.Car import HistCar
from operators.Models.Person import Person
from operators.Models.Person import HistPerson
from operators.Models.User import User
from operators.Models.User import HistUser

default_args = {'owner': 'sergio','start_date': datetime(2021, 2, 28)}
cfg = '/usr/local/airflow/dags/templates'


engine = create_engine(f'mysql://root:root@mysql_container:3306/cooler_car', pool_pre_ping=True)
Session = sessionmaker(bind=engine)
session = Session()

main_tables = []


def get_attibutes(clase):
    inst = inspect(clase)
    attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
    attr_names.remove('hash_key')
    attr_names.remove('created_at')
    attr_names.remove('updated_at')
    attr_names.remove('is_active')
    return attr_names


def read_files():
    list_of_catalogs = glob.glob(f'{cfg}/main_tables/*.csv')
    for row in list_of_catalogs:
        file_name = row.split(f'{cfg}/catalogs/')[1]
        table_name = file_name.split('.csv')[0]

        print(row, table_name)

        file_df = pd.read_csv(row, index_col=0)
    if table_name == 'BRANCH_OFFICE':
        rows_insert = []
        index_id = 1
        for information in file_df.itertuples():
            attribute = {'branch_office_id': index_id,
                         'branch_code': information[0]
                         }
            rows_insert.append(attribute)
            index_id = index_id + 1

        session.bulk_insert_mappings(BranchOffice, rows_insert)
        session.commit()
        session.close()

        rows_insert = []
        index_id = 1
        attr_names = get_attibutes(HistBranchOffice)

        attr_names.remove('branch_office_id')
        data = {}
        for index, row in file_df.iterrows():

            for att in attr_names:
                attribute = {att: file_df[att][index],
                             'hash_key': str(uuid.uuid4())
                             }

                data.update(attribute)
            data.update({'branch_office_id': index_id})
            rows_insert.append(data)
            data = {}
            index_id = index_id + 1

        session.bulk_insert_mappings(HistBranchOffice, rows_insert)
        session.commit()
        session.close()
    print('branch office')

    if table_name == 'CAR':
        rows_insert = []
        index_id = 1
        for information in file_df.itertuples():
            attribute = {'car_id': index_id
                         }
            rows_insert.append(attribute)
            index_id = index_id + 1

        session.bulk_insert_mappings(Car, data)
        session.commit()
        session.close()

        rows_insert = []
        index_id = 1
        attr_names = get_attibutes(HistCar)

        attr_names.remove('car_id')
        data = {}
        for index, row in file_df.iterrows():

            for att in attr_names:
                attribute = {att: file_df[att][index],
                             'hash_key': str(uuid.uuid4())
                             }

                data.update(attribute)
            data.update({'car_id': index_id})
            rows_insert.append(data)
            data = {}
            index_id = index_id + 1

        session.bulk_insert_mappings(HistCar, data)
        session.commit()
        session.close()

        print('+++++++++++')
        print(rows_insert)

    if table_name == 'USER':
        rows_insert = []
        index_id = 1
        for information in file_df.itertuples():
            attribute = {'user_id': index_id,
                         'email': information[0]
                         }
            rows_insert.append(attribute)
            index_id = index_id + 1

        session.bulk_insert_mappings(BranchOffice, data)
        session.commit()
        session.close()

        rows_insert = []
        index_id = 1
        attr_names = get_attibutes(HistBranchOffice)

        attr_names.remove('user_id')
        data = {}
        for index, row in file_df.iterrows():

            for att in attr_names:
                value = ''
                if att == 'user_type_id':

                    if file_df[att][index] == 'person':
                        value = '1'

                    if file_df[att][index] == 'partner':
                        value = '2'

                    if file_df[att][index] == 'system':
                        value = '3'

                    attribute = {att: value,
                                 'hash_key': str(uuid.uuid4())
                                 }
                else:
                    attribute = {att: file_df[att][index],
                                 'hash_key': str(uuid.uuid4())
                                 }

                data.update(attribute)
            data.update({'user_id': index_id})
            rows_insert.append(data)
            data = {}
            index_id = index_id + 1

        session.bulk_insert_mappings(HistBranchOffice, data)
        session.commit()
        session.close()

        print('+++++++++++')
        print(rows_insert)


with DAG('load-tables.py',
         default_args=default_args,
         schedule_interval=None,
         template_searchpath=cfg,
         catchup=False,
         is_paused_upon_creation=False) as dag:

    start = DummyOperator(task_id='start')

    load_files = PythonOperator(task_id='read_files_step',
                                python_callable=read_files)

    send_notification = EmailOperator(task_id='send_mail',
                                      to='sergiodavid.quintana@gmail.com',
                                      subject='load catalogs',
                                      html_content='<h1>load catalogs</h1>')

    end = DummyOperator(task_id='end')

start >> load_files >> send_notification >> end