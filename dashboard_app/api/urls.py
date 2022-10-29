from django.urls import path
from .views import ApisView



urlpatterns = [
    path('', ApisView.as_view(), name="apis"),
]
