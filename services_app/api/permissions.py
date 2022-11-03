from rest_framework.permissions import BasePermission

from services_app.models import Order


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
    def has_permission(self, request, view):
        # if request.method == "POST":
        #     return bool(
        #             request.user
        #             and request.user.is_authenticated
        #             and ((request.user.user_type == "3"
        #                     and request.user.customer_account == obj.offer.service.customer)
        #             )
        #         )
        return self.has_object_permission( request, view,Order.objects.get(id=view.kwargs.get("order_id")))
    def has_object_permission(self, request, view, obj):
        print(obj.offer.service.customer.id)
        return bool(
                request.user
                and request.user.is_authenticated
                and (
                        (request.user.user_type == "2"
                         and request.user.driver_account == obj.offer.driver)
                        or
                        (request.user.user_type == "3"
                         and request.user.customer_account == obj.offer.service.customer)
                )
            )
