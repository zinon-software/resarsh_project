from django.urls import path
from .views import UserApiView, UsersAPIView, UpgradeAccountToCustomerApiView, UpgradeAccountToDriverApiView



urlpatterns = [
    path('users/<str:username>/', UserApiView.as_view(), name="user"),
    path('users/', UsersAPIView.as_view(), name="users"),
    path('customer-upgrade/', UpgradeAccountToCustomerApiView.as_view(), name="customer-upgrade"),
    path('driver-upgrade/', UpgradeAccountToDriverApiView.as_view(), name="driver-upgrade"),
]
