from rest_framework.permissions import BasePermission

from services_app.models import Order


class UserIsNotCustomer(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            return bool(
                request.user
                and request.user.is_authenticated
                and request.user.user_type == "1"
            )
        if request.method == "PUT":
            return bool(
                request.user
                and request.user.is_authenticated
                and request.user.user_type == "3"
            )
        return True

class UserIsNotDriver(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            return bool(
                request.user
                and request.user.is_authenticated
                and request.user.user_type == "1"
            )
        if request.method == "PUT":
            return bool(
                request.user
                and request.user.is_authenticated
                and request.user.user_type == "2"
            )
        return True


