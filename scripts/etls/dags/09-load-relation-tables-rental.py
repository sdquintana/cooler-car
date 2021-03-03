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

from operators.Models.UserRent import Rent
from operators.Models.UserRent import RelUserRent


default_args = {'owner': 'sergio','start_date': datetime(2021, 2, 28)}
cfg = '/usr/local/airflow/dags/templates'


engine = create_engine(f'mysql://root:root@mysql_container:3306/cooler_car', pool_pre_ping=True)
Session = sessionmaker(bind=engine)
session = Session()

main_tables = []


def read_files():
    file_df = pd.read_csv(f'{cfg}/relation_tables/07-RENTAL.csv')

    index_id = 1

    row_insert = []
    row_insert_detail = []

    for row in file_df.itertuples():
        data = {'trip_id': row[1],
                'number': row[10]
                }

        row_insert.append(data)
        index_id = index_id + 1

    index_id = index_id = 1

    session.bulk_insert_mappings(Rent, row_insert)
    session.commit()

    for row in file_df.itertuples():

        data_detail = {'trip_id': row[1],
                       'user_id': row[2],
                       'hash_key': str(uuid.uuid4()),
                       'rental_date': row[3],
                       'delivery_date': row[4],
                       'branch_office_id': row[5],
                       'payment_method_id': row[6],
                       'fare': row[7],
                       'damage_fee': row[8],
                       'car_id': row[9]
                       }

        row_insert_detail.append(data_detail)
        index_id = index_id + 1

    session.bulk_insert_mappings(RelUserRent, row_insert_detail)
    session.commit()
    session.close()

    print(row_insert_detail)


with DAG('09-load-relation-tables-rental',
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