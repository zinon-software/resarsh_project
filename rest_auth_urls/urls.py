"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_auth.registration.views import RegisterView, VerifyEmailView
from rest_auth.views import LoginView, LogoutView, PasswordChangeView, UserDetailsView
from django.views.generic import TemplateView


# from django.conf.urls import url

urlpatterns = [
    path("registration/", RegisterView.as_view(), name="rest_register"),
    path(
        "registration/verify-email/",
        VerifyEmailView.as_view(),
        name="rest_verify_email",
    ),
    path(
        "registration/account-confirm-email/<str:key>/",
        TemplateView.as_view(template_name="account-confirm.html"),
        name="account_confirm_email",
    ),
    path("login/", LoginView.as_view(), name="rest_login"),
    # URLs that require a user to be logged in with a valid session / token.
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
    path("password/change/", PasswordChangeView.as_view(), name="rest_password_change"),

]

