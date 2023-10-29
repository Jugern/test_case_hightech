from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import InactiveUser
from django import forms
import random
import string

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username", "email")

class ChangesForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')
    username = forms.CharField(max_length=30, label='Логин')
    email = forms.EmailField(label='Введите Email адрес')
    password = forms.CharField(widget=forms.PasswordInput(), label='Введите пароль')
    password_confirmation = forms.CharField(widget=forms.PasswordInput(), label='Повторите пароль')
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже зарегистрирован")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Пароли не совпадают")
        username = 'your_username'
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь существует.")

    def save(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        activation_token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=64))
        inactive_user = InactiveUser.objects.create(user=user, activation_token=activation_token)
        inactive_user.save()

        return user