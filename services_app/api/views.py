import django_filters
from django.utils import timezone
from xmlrpc.client import DateTime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import permissions, status, filters

from services_app.api.permissions import CustomerOnlyObject, DriverOnlyObject, DriverOrCustomerOnlyObject
from services_app.api.serializers import OfferSerializers, OrderSerializers, ServiceSerializers
from services_app.models import Offer, Order, Service
from account_app.api.views import set_request_data
from rest_framework import generics


class ServicesAPIView(generics.ListCreateAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, CustomerOnlyObject]
    serializer_class = ServiceSerializers
    customer_field = 'customer'

    queryset = Service.objects.all()

    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['customer__user__username' ]#, 'cargo_type']
    def get_queryset(self):
        queryset = Service.objects.all()
        customer__user = self.request.query_params.get('customer__user__username')
        if customer__user is not None:
            print(customer__user)
            queryset = queryset.filter(customer__user__username=customer__user)
        return queryset

    def get(self, request, *args, **kwargs):
        services = Service.objects.all()

        serializer = ServiceSerializers(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request = set_request_data(
            request, request.user.customer_account.id, 'customer')
        serializer = ServiceSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceApiView(APIView):
    permission_classes = [CustomerOnlyObject]
    serializer_class = ServiceSerializers
    customer_field = 'customer'

    def get_object(self, service_id):
        '''
        Helper method to get the object with given  user
        '''
        try:
            return Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return None

    def get(self, request, service_id, *args, **kwargs):

        user_instance = self.get_object(service_id)
        if not user_instance:
            return Response(
                {"message": "الخدمة غير موجود"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ServiceSerializers(user_instance)

        return Response(serializer.data, status=status.HTTP_200_OK)


class OffersAPIView(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, DriverOnlyObject]
    serializer_class = OfferSerializers
    driver_field = 'driver'

    def get(self, request, *args, **kwargs):
        offerts = Offer.objects.all()

        serializer = OfferSerializers(offerts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request = set_request_data(
            request, request.user.driver_account.id, 'driver')
        serializer = OfferSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfferApiView(APIView):
    permission_classes = [DriverOnlyObject]
    serializer_class = OfferSerializers
    driver_field = 'driver'

    def get_object(self, offer_id):
        '''
        Helper method to get the object with given  user
        '''
        try:
            return Offer.objects.get(id=offer_id)
        except Offer.DoesNotExist:
            return None

    def get(self, request, offer_id, *args, **kwargs):

        user_instance = self.get_object(offer_id)
        if not user_instance:
            return Response(
                {"message": "العرض غير موجود"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OfferSerializers(user_instance)

        return Response(serializer.data, status=status.HTTP_200_OK)


class OrdersAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = OrderSerializers

    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()

        serializer = OrderSerializers(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request = set_request_data(
            request, request.user.customer_account.id, 'customer')
        serializer = OrderSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderAPIView(APIView):
    permission_classes = [DriverOrCustomerOnlyObject]
    serializer_class = OrderSerializers

    def get_object(self, order_id):
        '''
        Helper method to get the object with given  user
        '''
        try:
            return Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return None

    def get(self, request, order_id, *args, **kwargs):

        order_instance = self.get_object(order_id)
        if not order_instance:
            return Response(
                {"message": "الطلب غير موجود"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OrderSerializers(order_instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, order_id, *args, **kwargs):
        '''
        Updates the todo item with given order_id if exists
        '''
        order_instance = self.get_object(order_id)
        if not order_instance:
            return Response({"message": "الطلب غير موجود"}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'order_status': request.data.get('order_status'),
        }
        if (request.data.get('order_status') == 'complete'):
            data.update({
                'order_status': request.data.get('order_status'),
                'arrival_dt': timezone.now()
            })

        serializer = OrderSerializers(
            instance=order_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, order_id, *args, **kwargs):
    #     order_instance = self.get_object(order_id)
    #     if not order_instance:
    #         return Response(
    #             {"res": "الطلب غير موجود"},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     order_instance.delete()
    #     return Response({'message': "تم حذف الطلب"}, status=status.HTTP_200_OK)


class MyServicesAPIView(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, CustomerOnlyObject]
    serializer_class = ServiceSerializers

    def get(self, request, *args, **kwargs):
        request = set_request_data(
            request, request.user.customer_account.id, 'customer')
        services = Service.objects.filter(customer__user = request.user)

        serializer = ServiceSerializers(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        request = set_request_data(
            request, request.user.customer_account.id, 'customer')
        serializer = ServiceSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


