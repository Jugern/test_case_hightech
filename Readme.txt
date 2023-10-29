Тестовое задание для Hightech.

Для начало использования через Docker-container,
задайте ниже следующие значения в .env файле

#python setting
debug=1 #это оставляете как есть
secret_key="секретный ключ"
allowed_hosts="хосты на котором работают через запятую" #например localhost,127.0.0.1
site_url="домен своего сайта"

#db postgresql
db_engine=django.db.backends.postgresql #это оставляете как есть
db_name="Имя базы данных"
db_user="Логин базы данных"
db_pass="Пароль базы данных"
db_host="хост базы данных"
db_port="Порт базы данных PostgreSQL"

#smtp
e_host="Хост вашей почты"
e_port="ПОРТ SMTP вашей почты"
e_host_user="Электронная почта"
e_host_password="Пароль от почты"
e_use_ssl=True
def_from_e="Электронная почта"

