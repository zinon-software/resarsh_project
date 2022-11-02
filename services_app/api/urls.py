from django.urls import path

from services_app.api.views import OfferApiView, OffersAPIView, OrderAPIView, OrdersAPIView, ServiceApiView, ServicesAPIView



urlpatterns = [
    path('services/', ServicesAPIView.as_view(), name="services"),
    path('services/<int:service_id>/', ServiceApiView.as_view(), name="service"),
    path('offers/', OffersAPIView.as_view(), name="offers"),
    path('offers/<int:offer_id>/', OfferApiView.as_view(), name="offer"),
    path('orders/', OrdersAPIView.as_view(), name="orders"),
    path('orders/<int:order_id>/', OrderAPIView.as_view(), name="order"),
]
