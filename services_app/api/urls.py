from django.urls import path

from services_app.api.views import ServiceApiView, ServicesAPIView



urlpatterns = [
    path('', ServicesAPIView.as_view(), name="services"),
    path('<int:service_id>/', ServiceApiView.as_view(), name="service"),
]
