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

from operators.Models.Person import Person
from operators.Models.Person import HistPerson

default_args = {'owner': 'sergio','start_date': datetime(2021, 2, 28)}
cfg = '/usr/local/airflow/dags/templates'

database = Variable.get('mysql_vars', deserialize_json=True)
email = Variable.get('email', deserialize_json=True)

engine = create_engine(f"mysql://{database['user']}:{database['password']}@{database['host']}:3306/{database['schema']}")
Session = sessionmaker(bind=engine)
session = Session()

main_tables = []


def read_files():
    file_df = pd.read_csv(f'{cfg}/main_tables/04-PERSON.csv')

    index_id = 1

    row_insert = []
    row_insert_detail = []

    for row in file_df.itertuples():
        data = {'person_id': index_id}

        row_insert.append(data)
        index_id = index_id + 1



    session.bulk_insert_mappings(Person, row_insert)
    session.commit()

    index_id = index_id = 1

    for row in file_df.itertuples():

        value = ''
        if row[9] == 'PF':
            value = '1'

        if row[9] == 'PFAE':
            value = '2'

        if row[9] == 'PM':
            value = '3'

        data_detail = {'person_id': index_id,
                       'hash_key': str(uuid.uuid4()),
                       'user_id': row[1],
                       'name': row[2],
                       'second_name': row[3],
                       'last_name': row[4],
                       'second_last_name': row[5],
                       'curp': row[6],
                       'rfc': row[7],
                       'ine_number': row[8],
                       'person_type_id': value
                       }

        row_insert_detail.append(data_detail)
        index_id = index_id + 1

    session.bulk_insert_mappings(HistPerson, row_insert_detail)
    session.commit()
    session.close()

    print(row_insert_detail)


with DAG('06-load-main-tables-person',
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
                                      subject='load person table',
                                      html_content='<h1>load person table</h1>')

    end = DummyOperator(task_id='end')

start >> load_files >> send_notification >> end