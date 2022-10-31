from rest_framework.permissions import BasePermission


class CustomerOnlyObject(BasePermission):
    """
    Allows access only to vendors.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return bool(
                request.user
                and request.user.is_authenticated
                and request.user.user_type == "3"
            )
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.user_type == "3"  # التاكد ان نوع المستخدم customer
            and request.user.customer_account == getattr(obj, getattr(view, "customer_field", "customer"))
            # التاكد ان صاحب الخدمة هو نفسه من يعدل عليها
        )


class DriverOnlyObject(BasePermission):
    """
    Allows access only to Drivers.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return bool(
                request.user
                and request.user.is_authenticated
                and request.user.user_type == "2"
            )
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.user_type == "2"  # التاكد ان نوع المستخدم driver
            and request.user.driver_account == getattr(obj, getattr(view, "driver_field", "driver"))
            # التاكد ان صاحب العرض هو نفسه من يعدل عليها
        )


class DriverOrCustomerOnlyObject(BasePermission):
    """
    Allows access only to Order Driver or Order Customer.
    """

    def has_object_permission(self, request, view, obj):
        if request.method == "PUT":
            return bool(
                request.user
                and request.user.is_authenticated
                and (
                        (request.user.user_type == "2"
                         and request.user.driver_account == getattr(obj, 'driver_account',False))
                        or
                        (request.user.user_type == "3"
                         and request.user.customer_account == getattr(obj,'customer_account',False))
                )
            )
