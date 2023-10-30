#Тестовое задание для Hightech.

#Для начало использования через Docker-container,
#создайте и задайте ниже следующие значения в .env файле

#python setting
#это оставляете как есть
debug=1
#секретный ключ джанго
secret_key=key
#хосты на котором работает django, через запятую. Например: localhost,127.0.0.1
allowed_hosts=localhost,127.0.0.1
#домен своего сайта
site_url=example.com

#заполнение db postgresql
#не изменяем
db_engine=django.db.backends.postgresql
#Имя базы данных, юзер и пароль
db_name=name
db_user=user
db_pass=pass
#не изменяем
db_host=db
#Порт базы данных PostgreSQL (обычно 5432)
db_port=port

#smtp для почты
#Хост вашей почты
e_host=smtp.email.com
#ПОРТ SMTP вашей почты
e_port=port
#Электронная почта
e_host_user=email.example.com
#Пароль от почты
e_host_password=password
#не изменяем
e_use_ssl=True
#Электронная почта
def_from_e=email.example.com

