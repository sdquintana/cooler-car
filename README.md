# Cooler Car

## Instructions

> ### 1. Startup platform
Move to path: projet_path/cooler-car/docker/cooler-car-platform
`cd projet_path/cooler-car/docker/cooler-car-platform`


- Build docker images.

`docker build -t custom-airflow .`

- Execute docker.

`docker-compose up -d --remove-orphans` 

- Move to projet_path/cooler-car/scripts/install

`cd projet_path/cooler-car/scripts/install`

- Set Execution permission to add_coneccion.sh

`chmod +x add_coneccion.sh`

- Open docker/cooler-car-platform/variables/email.json and edit tag for your email

- Execution script

`./add_coneccion`

- Verify if mysql is ready and wait until mysql is running ok (check running /docker-entrypoint-initdb.d/cooler-car-model_create.sql script was executed
and wait for message [Server] Insecure configuration for --pid-file: Location '/var/run/mysqld' in the path is accessible to all OS users. Consider choosing a different directory. appears to times).

`docker logs cooler-car-platform_mysql_container_1 -f`


> ### 2. Create a virtual environment

- Move to path project_path/cooler-car/scripts/python/scrapper

`cd project_path/cooler-car/scripts/python/scrapper`

- Create virtual environment.

`python3 -m venv $PWD/venv`  

> ### 3. execute scrapper to load trademarks

- Move to project_path/cooler-car/scripts/python/scrapper 

`cd project_path/cooler-car/scripts/python/scrapper`

- Load virtual env.

`source venv/bin/activate`

- Install dependencies.

`pip install -r requirements.txt`

- Run scrapper.

`python load-trademarks.py`

> Note: this step might crashes; due to google driver version if this crashes you can
> can run etl-dag 01-load-catalogs-custom. but this step runs ok ignore 01-load-catalogs-custom

> ### 4. Execution dags

- Open a web browser url http://localhost:8080/

- Click on `02-load-catalogs > Trigger DAG > Trigger` and wait for all steps fished

- Repeats this for any numeral dags.


> ### 5. Check Results

- Create a connection of mysql using:

`mysql -h 127.0.0.1 -u root -P 3306 -p` 

- enter root

una vez adentro

`use dim`

`select * from  DIM.AGG_RENTALS;`



