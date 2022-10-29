from django.urls import path
from .views import UserApiView



urlpatterns = [
    path('user/<str:username>/', UserApiView.as_view(), name="user"),
]
