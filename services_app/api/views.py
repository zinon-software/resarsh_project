
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import permissions, status

from dashboard_app.api.views import ApisView
from services_app.api.permissions import CustomerOnlyObject, DriverOnlyObject
from services_app.api.serializers import OfferSerializers, ServiceSerializers
from services_app.models import Offer, Service
from account_app.api.views import set_request_data

class ServicesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,CustomerOnlyObject]
    serializer_class = ServiceSerializers
    customer_field = 'customer'

    def get(self, request, *args, **kwargs):
        services = Service.objects.all()

        serializer = ServiceSerializers(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request = set_request_data(request,request.user.customer_account.id,'customer')
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
                {"res": "الخدمة غير موجود"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ServiceSerializers(user_instance)

        return Response(serializer.data, status=status.HTTP_200_OK)



class OffersAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,DriverOnlyObject]
    serializer_class = OfferSerializers
    driver_field = 'driver'

    def get(self, request, *args, **kwargs):
        offerts = Offer.objects.all()

        serializer = OfferSerializers(offerts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request = set_request_data(request,request.user.driver_account.id,'driver')
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
        except Service.DoesNotExist:
            return None

    def get(self, request, offer_id, *args, **kwargs):

        user_instance = self.get_object(offer_id)
        if not user_instance:
            return Response(
                {"res": "الخدمة غير موجود"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OfferSerializers(user_instance)

        return Response(serializer.data, status=status.HTTP_200_OK)



