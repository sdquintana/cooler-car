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
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator

from operators.Models.BranchOffice import BranchOffice
from operators.Models.BranchOffice import HistBranchOffice

default_args = {'owner': 'sergio','start_date': datetime(2021, 2, 28)}
cfg = '/usr/local/airflow/dags/templates'

database = Variable.get('mysql_vars', deserialize_json=True)
email = Variable.get('email', deserialize_json=True)

engine = create_engine(f"mysql://{database['user']}:{database['password']}@{database['host']}:3306/{database['schema']}")
Session = sessionmaker(bind=engine)
session = Session()

main_tables = []


def read_files():
    file_df = pd.read_csv(f'{cfg}/main_tables/01-BRANCH_OFFICE.csv')

    index_id = 1

    row_insert = []
    row_insert_detail = []

    for row in file_df.itertuples():
        data = {'branch_office_id': index_id,
                'branch_code': row[1]}

        row_insert.append(data)
        index_id = index_id + 1

    session.bulk_insert_mappings(BranchOffice, row_insert)
    session.commit()

    index_id = index_id = 1

    for row in file_df.itertuples():

        data_detail = {'branch_office_id': index_id,
                       'hash_key': str(uuid.uuid4()),
                       'name': row[2],
                       'address_1': row[3],
                       'address_2': row[4],
                       'cp': row[5],
                       'city': row[6],
                       'state': row[7],
                     }

        row_insert_detail.append(data_detail)
        index_id = index_id + 1

    session.bulk_insert_mappings(HistBranchOffice, row_insert_detail)
    session.commit()
    session.close()

    print(row_insert_detail)


with DAG('04-load-main-tables-branch',
         default_args=default_args,
         schedule_interval=None,
         template_searchpath=cfg,
         catchup=False,
         is_paused_upon_creation=False) as dag:

    start = DummyOperator(task_id='start')

    load_files = PythonOperator(task_id='read_files_step',
                                python_callable=read_files)

    send_notification = EmailOperator(task_id='send_mail',
                                      to=f"{email['email']}",
                                      subject='load branch office table',
                                      html_content='<h1>load branch office table</h1>')

    end = DummyOperator(task_id='end')

start >> load_files >> send_notification >> end