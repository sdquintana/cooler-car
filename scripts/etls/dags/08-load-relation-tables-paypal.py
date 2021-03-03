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

from operators.Models.PayPalAccount import PayPalAccount
from operators.Models.PayPalAccount import RelPayPalAccount
from operators.Models.PaymentMethod import PaymentMethod

default_args = {'owner': 'sergio','start_date': datetime(2021, 2, 28)}
cfg = '/usr/local/airflow/dags/templates'


engine = create_engine(f'mysql://root:root@mysql_container:3306/cooler_car', pool_pre_ping=True)
Session = sessionmaker(bind=engine)
session = Session()

main_tables = []


def read_files():
    file_df = pd.read_csv(f'{cfg}/relation_tables/06-PAYPAL_ACCOUNT.csv')
    index_id = 1

    row_insert = []
    row_insert_detail = []

    for row in file_df.itertuples():
        data = {'paypal_account_id': index_id,
                'email': row[1],
                'password': row[2]}

        row_insert.append(data)
        index_id = index_id + 1

    session.bulk_insert_mappings(PayPalAccount, row_insert)
    session.commit()

    index_payment_method_id = pd.read_sql_query(f"""select max(payment_method_id) id from cooler_car.CAT_PAYMENT_METHOD """, engine)

    index_payment_method_id = 0 if index_payment_method_id['id'][0] is None else int(index_payment_method_id['id'])

    row_insert = []
    index_payment_method_id = index_payment_method_id +1
    for row in file_df.itertuples():
        data = {'payment_method_id': index_payment_method_id,
                'payment_method_type_id': 2}

        row_insert.append(data)
        index_payment_method_id = index_payment_method_id + 1

    session.bulk_insert_mappings(PaymentMethod, row_insert)
    session.commit()

    index_id = index_id = 1
    index_payment_method_id = pd.read_sql_query(
        f"""select max(payment_method_id) id from cooler_car.CAT_PAYMENT_METHOD """, engine)

    index_payment_method_id = 0 if index_payment_method_id['id'][0] is None else int(index_payment_method_id['id'])

    for row in file_df.itertuples():

        data_detail = {'payment_method_id': index_payment_method_id,
                       'paypal_account_id': index_id,
                       'hash_key': str(uuid.uuid4())
                       }

        row_insert_detail.append(data_detail)
        index_id = index_id + 1

    session.bulk_insert_mappings(RelPayPalAccount, row_insert_detail)
    session.commit()
    session.close()

    print(row_insert_detail)


    print(row_insert_detail)


with DAG('08-load-relation-tables-paypal',
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