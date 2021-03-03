import time
import os

from datetime import datetime

import pendulum

local_tz = pendulum.timezone("America/Mexico_City")


from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator
from airflow.utils.dates import days_ago


default_args = {'owner': 'sergio',
                'start_date': datetime(2020, 10, 1, tzinfo=local_tz)
                }


def hello_world_loop():
    for palabra in ['hello', 'world']:
        print(palabra)


with DAG('a-test',
         default_args=default_args,
         schedule_interval=None,
         catchup=False) as dag:
    start = DummyOperator(task_id='start')

    prueba_python = PythonOperator(task_id='prueba_python',
                                   python_callable=hello_world_loop)

    prueba_bash = BashOperator(task_id='prueba_bash',
                               bash_command='echo prueba_bash')

    send_notification = EmailOperator(task_id='send_mail',
                                      to='netrerseo@gmail.com,sergiodavid.quintana@gmail.com',
                                      subject='test',
                                      html_content='<h1>test</h1>')

start >> prueba_python >> prueba_bash >> send_notification