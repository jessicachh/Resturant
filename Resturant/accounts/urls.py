from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path("register/",register,name="register"),
    path("login/",log_in,name="login"),
    path("logout/",log_out,name="log_out"),
    path("change_password/",change_password,name="change_password"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_done.html"), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('profile_dashboard/',profile_dashboard,name="profile_dashboard"),
    path('profile/',profile,name="profile")

]
