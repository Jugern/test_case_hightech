from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from os import environ
from djangoProject.settings import EMAIL_HOST_USER, SITE_URL

def send_confirmation_email(token, request):
    subject = 'Подтверждение изменения email-адреса'
    from_email = EMAIL_HOST_USER
    to_email = token.user.email

    # Создание контекста для шаблона письма
    context = {
        'token': token.key,
        'user': token.user,
        'setting': SITE_URL,
    }

    # Загрузка шаблона письма
    email_body = render_to_string('registration/confirmation_email.html', context, request=request)
    # Создание объекта EmailMessage и отправка письма
    email = EmailMessage(subject, email_body, from_email, [to_email])
    email.send()


def signup_email(data, request):
    subject = 'Подтверждение изменения email-адреса'
    from_email = EMAIL_HOST_USER
    to_email = data['email']

    context = {
        'user': data['user'],
        'email': data['email'],
        'setting': SITE_URL,
    }

    email_body = render_to_string('registration/signup_email_registration.html', context, request=request)
    email = EmailMessage(subject, email_body, from_email, [to_email])
    email.send()