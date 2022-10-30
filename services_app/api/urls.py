from django.urls import path

from services_app.api.views import OfferApiView, OffersAPIView, ServiceApiView, ServicesAPIView



urlpatterns = [
    path('', ServicesAPIView.as_view(), name="services"),
    path('<int:service_id>/', ServiceApiView.as_view(), name="service"),
    path('offers/', OffersAPIView.as_view(), name="services"),
    path('offers/<int:offer_id>/', OfferApiView.as_view(), name="service"),
]
