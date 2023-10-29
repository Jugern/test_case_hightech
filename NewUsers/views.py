from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import CreationForm, ChangesForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import EmailChangeToken
from .utils import send_confirmation_email, signup_email
from datetime import timedelta
from django.utils.crypto import get_random_string


def main(request):
    return render(request, 'main.html')


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.POST:
            context = {
                'user': request.POST['username'],
                'email': request.POST['email']
            }
            signup_email(context, request)
        return response


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


def email_setting_done(request):
    return render(request, 'registration/email_setting_done.html')
