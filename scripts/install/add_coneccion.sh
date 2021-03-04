server="docker ps -aqf name=cooler-car-platform_webserver_1"
eval "$server"
server_name=$(eval "$server")
docker exec -it -u root $server_name airflow connections --add --conn_id cool_car --conn_uri mysql://root:root@mysql_container:3306/cooler_car
docker exec -it -u root $server_name airflow variables -i /usr/local/airflow/variables/mysql.json
docker exec -it -u root $server_name airflow variables -i /usr/local/airflow/variables/email.json