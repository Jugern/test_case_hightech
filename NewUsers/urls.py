from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ex: /polls/
    path('', views.main, name='main'),
    path('all_users', views.all_users, name='all_users'),
    path('activate/<uuid:id>/<str:token>/', views.activate, name='activate'),
    path("auth/sign_up", views.register, name='signup'),
    path('user/email_setting', views.email_setting, name='email_setting'),
    path('user/email_setting_done', views.email_setting_done, name='email_setting_done'),
    path('user/confirm_email_change/<str:token>', views.confirm_email_change, name='confirm_email_change'),
    path('user/<uuid:id>/', views.user_info, name='user_info'),
    path('user/setting', views.user_setting, name='user_setting'),
    path("auth/", include("django.contrib.auth.urls")),
    ]