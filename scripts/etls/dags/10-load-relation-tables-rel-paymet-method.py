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


from operators.Models.PaymentMethod import RelPaymentMethod


default_args = {'owner': 'sergio','start_date': datetime(2021, 2, 28)}
cfg = '/usr/local/airflow/dags/templates'


engine = create_engine(f'mysql://root:root@mysql_container:3306/cooler_car', pool_pre_ping=True)
Session = sessionmaker(bind=engine)
session = Session()

main_tables = []


def read_files():
    file_df = pd.read_csv(f'{cfg}/relation_tables/08-REL_PAYMENT_METHOD.csv')

    index_id = 1

    row_insert = []
    row_insert_detail = []

    for row in file_df.itertuples():

        data_detail = {'wallet_id': row[1],
                       'payment_method_id': row[2],
                       'user_id': row[3],
                        'hash_key': str(uuid.uuid4()),
                       'principal': row[4]
                       }

        row_insert_detail.append(data_detail)
        index_id = index_id + 1

    session.bulk_insert_mappings(RelPaymentMethod, row_insert_detail)
    session.commit()
    session.close()

    print(row_insert_detail)


with DAG('10-load-relation-tables-rel-paymet-method',
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