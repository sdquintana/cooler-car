import glob
import pandas as pd
import numpy as np

from datetime import datetime
from sqlalchemy import exc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from airflow.models import DAG
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator

default_args = {'owner': 'sergio','start_date': datetime(2021, 2, 28) }
cfg = '/usr/local/airflow/dags/templates'

database = Variable.get('mysql_vars', deserialize_json=True)
email = Variable.get('email', deserialize_json=True)

engine = create_engine(f"mysql://{database['user']}:{database['password']}@{database['host']}:3306/{database['schema']}")
Session = sessionmaker(bind=engine)
session = Session()


def read_files():

    list_of_catalogs = glob.glob(f'{cfg}/catalogs/*.csv')

    for row in list_of_catalogs:
        file_name = row.split(f'{cfg}/catalogs/')[1]
        table_name = file_name.split('.csv')[0]

        print(row, table_name)

        file_df = pd.read_csv(row, index_col=0)

        file_df.to_sql(table_name, engine, schema='cooler_car', if_exists='append')

    print('ready')


with DAG('02-load-catalogs',
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
                                      subject='load catalogs',
                                      html_content='<h1>load catalogs</h1>')

    end = DummyOperator(task_id='end')

start >> load_files >> send_notification >> end