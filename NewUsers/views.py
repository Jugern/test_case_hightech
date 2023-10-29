from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from .forms import CreationForm, ChangesForm, RegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.timezone import now
from .models import EmailChangeToken, InactiveUser
from .utils import send_confirmation_email, signup_email
from datetime import timedelta
from django.utils.crypto import get_random_string
from decorators.decorators import anonymous_required
from uuid import uuid4
from djangoProject.settings import EMAIL_HOST_USER
from decorators.decorators import anonymous_required


def main(request):
    return render(request, 'main.html')


# class SignUp(CreateView):
#     form_class = CreationForm
#     success_url = reverse_lazy("login")
#     template_name = "registration/signup.html"
#
#     def dispatch(self, request, *args, **kwargs):
#         response = super().dispatch(request, *args, **kwargs)
#         if request.POST:
#             context = {
#                 'user': request.POST['username'],
#                 'email': request.POST['email']
#             }
#             signup_email(context, request)
#         return response


@login_required
def all_users(request):
    return render(request, 'all_users.html', {"auth": 1})


@login_required
def user_info(request, id):
    User = get_user_model()
    info = User.objects.get(id=id)
    if not info.email:
        info.email = 'email не введен!'
    if str(request.user) == info.username:
        return render(request, 'user_info.html', {'info': info, 'account': 1})
    else:
        return render(request, 'user_info.html', {'info': info})


@login_required
def user_setting(request):
    User = get_user_model()
    info = User.objects.get(username=request.user)
    error = ""
    if request.method == 'POST':
        form = ChangesForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_info', id=info.id)
        else:
            error = 'Такой пользователь уже есть'
            return render(request, 'user_setting.html', {'form': form, 'info': info, 'error': error})
    form = ChangesForm(instance=request.user)
    return render(request, 'user_setting.html', {'form': form, 'info': info, 'error': error})


@login_required
def email_setting(request):
    if request.method == 'POST':
        new_email = request.POST['new_email']
        token = EmailChangeToken.objects.create(
            user=request.user,
            old_email=request.user.email,
            new_email=new_email,
            expires_at=now() + timedelta(minutes=20),
            key=get_random_string(32)
        )
        send_confirmation_email(token, request)  # Отправка письма с подтверждением
        token.save()
        return redirect('email_setting_done')
    return render(request, 'registration/email_setting.html')

@login_required()
def confirm_email_change(request, token):
    try:
        token = EmailChangeToken.objects.get(key=token, is_expired=False)
        if now() > token.expires_at:
            token.is_expired = True
            token.delete()
            return render(request, 'registration/email_change_expired.html')
        else:
            user = token.user
            user.email = token.new_email
            user.save()
            token.is_expired = True
            token.delete()
            return render(request, 'registration/email_change_success.html', {'user': user})
    except EmailChangeToken.DoesNotExist:
        return render(request, 'registration/email_change_invalid.html')

@login_required()
def email_setting_done(request):
    return render(request, 'registration/email_setting_done.html')


@anonymous_required
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            mail_subject = 'Активация аккаунта на сайте {}'.format(current_site.name),
            uid = str(user.id)
            message = render_to_string('registration/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'to': user.email,
                'uid': uid,
                'token': InactiveUser.objects.get(user=user).activation_token,
            }, request=request)
            # signup_email(message, request)
            email = EmailMessage(mail_subject, message, EMAIL_HOST_USER, [user.email])
            email.send()
            messages.success(request, 'Письмо с подтверждением отправлено на ваш email-адрес.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})

@anonymous_required
def activate(request, id, token):
    try:
        User = get_user_model()
        user = User.objects.get(id=id)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    try:

        if user is not None and InactiveUser.objects.get(user=user).activation_token == token:
            inactive_user = InactiveUser.objects.get(user=user)
            if inactive_user:
                inactive_user.delete()

            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'Ваш аккаунт был успешно активирован.')
            return redirect('main')
        else:
            messages.error(request, 'Ссылка для активации недействительна или истек срок её действия.')
            return redirect('main')
    except:
        messages.error(request, 'Ошибка подтверждения!.')
        return redirect('main')




