from rest_framework.permissions import BasePermission

from services_app.models import Order


class UserIsNotCustomerOrDriver(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            return bool(
                request.user
                and request.user.is_authenticated
                and request.user.user_type == "1"
            )
        return True


