import django_filters
from django.utils import timezone
from xmlrpc.client import DateTime

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import permissions, status
from services_app.api.pagination import CustomPagination

from services_app.api.permissions import CustomerOnlyObject, DriverOnlyObject, DriverOrCustomerOnlyObject
from services_app.api.serializers import OfferSerializers, OrderSerializers, ServiceSerializers
from services_app.models import Offer, Order, Service
from account_app.api.views import set_request_data
from rest_framework import generics

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

class ServicesAPIView(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, CustomerOnlyObject]
    serializer_class = ServiceSerializers
    customer_field = 'customer'

    queryset = Service.objects.all()
    
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('id', 'customer__user__username', 'cargo_type')


    pagination_class = CustomPagination
    
    
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



class OffersAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, DriverOnlyObject]
    queryset = Offer.objects.all()
    serializer_class = OfferSerializers
    driver_field = 'driver'

    filter_backends = (DjangoFilterBackend, SearchFilter)

    filterset_fields = ('id', 'service', 'driver','driver__user__username', 'service__customer', 'service__customer__user__username')


    pagination_class = CustomPagination


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




class OrdersAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = OrderSerializers

    pagination_class = CustomPagination

    queryset = Order.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)

    filterset_fields = ('id', 'offer', 'order_status', 'offer__driver', 'offer__driver__user__username',
     'offer__service', 'offer__service__customer', 'offer__service__customer__user__username')


    def post(self, request, format=None):
        request = set_request_data(request, request.user.customer_account.id, 'customer')
        serializer = OrderSerializers(data=request.data,context={"request":request})
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

        serializer = OrderSerializers(instance=order_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





