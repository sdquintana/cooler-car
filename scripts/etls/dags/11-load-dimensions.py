import pandas as pd
import pendulum
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from datetime import datetime


from airflow.models import DAG
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from airflow.operators.mysql_operator import MySqlOperator

email = Variable.get('email', deserialize_json=True)


local_tz = pendulum.timezone("America/Mexico_City")

cfg = '/usr/local/airflow/dags/templates/sql_scritps'
default_args = {'owner': 'sergio', 'start_date': datetime(2021, 3, 1, tzinfo=local_tz)}


with DAG('11-load-dimensions.py',
         default_args=default_args,
         schedule_interval=None,
         template_searchpath=cfg,
         catchup=False,
         is_paused_upon_creation=False) as dag:

    start = DummyOperator(task_id='start')

    truncate_tables = MySqlOperator(task_id='truncate_tables',
                                    mysql_conn_id='cool_car',
                                    sql='00-truncate_tables.sql',
                                    autocommit=True,
                                    dag=dag)

    load_branch = MySqlOperator(task_id='load_branch_office',
                                    mysql_conn_id='cool_car',
                                    sql='01-dim_branch_office.sql',
                                    autocommit=True,
                                    dag=dag)

    load_car = MySqlOperator(task_id='load_car',
                                mysql_conn_id='cool_car',
                                sql='02-dim_car.sql',
                                autocommit=True,
                                dag=dag)

    load_payment_method = MySqlOperator(task_id='load_payment_method',
                             mysql_conn_id='cool_car',
                             sql='03-dim_payment_method.sql',
                             autocommit=True,
                             dag=dag)

    load_person = MySqlOperator(task_id='load_person',
                                        mysql_conn_id='cool_car',
                                        sql='04-dim_person.sql',
                                        autocommit=True,
                                        dag=dag)

    load_rental = MySqlOperator(task_id='load_rental',
                                mysql_conn_id='cool_car',
                                sql='05-dim_rental.sql',
                                autocommit=True,
                                dag=dag)

    load_user = MySqlOperator(task_id='load_user',
                                mysql_conn_id='cool_car',
                                sql='06-dim_user.sql',
                                autocommit=True,
                                dag=dag)

    load_agg = MySqlOperator(task_id='load_agg',
                              mysql_conn_id='cool_car',
                              sql='07-agg_rentals.sql',
                              autocommit=True,
                              dag=dag)

    send_notification = EmailOperator(task_id='send_mail',
                                      to=f"{email['email']}",
                                      subject='load dimensions tables',
                                      html_content='<h1>load dimensions tables</h1>')

    end = DummyOperator(task_id='end')


start >> truncate_tables >> \
        load_branch >> \
        load_car >> \
        load_payment_method >> \
        load_person >> \
        load_rental >> \
        load_user >> \
        load_agg >>\
        send_notification >>\
end

