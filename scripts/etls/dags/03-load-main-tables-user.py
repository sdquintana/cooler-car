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
    file_df = pd.read_csv(f'{cfg}/main_tables/03-USER.csv')

    index_id = 1

    row_insert = []
    row_insert_detail = []

    for row in file_df.itertuples():
        data = {'user_id': index_id ,
                'email': row[1]
                }

        row_insert.append(data)
        index_id = index_id + 1

    index_id = index_id = 1

    session.bulk_insert_mappings(User, row_insert)
    session.commit()

    for row in file_df.itertuples():

        value = ''
        if row[4] == 'person':
            value = '1'

        if row[4] == 'partner':
            value = '2'

        if row[4] == 'system':
            value = '3'

        data_detail = {'user_id': index_id ,
                       'hash_key': str(uuid.uuid4()),
                       'password': row[2],
                       'phone': row[3],
                       'user_type_id': value
                       }

        row_insert_detail.append(data_detail)
        index_id = index_id + 1

    session.bulk_insert_mappings(HistUser, row_insert_detail)
    session.commit()
    session.close()

    print(row_insert_detail)


with DAG('03-load-main-tables-user',
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