
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import generics

from rest_framework import permissions, status
from account_app.api.permissions import UserIsNotCustomer, UserIsNotDriver
from account_app.api.serializers import DriverSerializers, UserSerializers, CustomerSerializers

from account_app.models import Customer, Driver, User
from services_app.api.pagination import CustomPagination


from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


def set_request_data(request,value=None,user_field_name='user'):
    "Set user from request"
    try:
        # сhange the values you want
        request.data[user_field_name] = value
    except:
        # remember old state
        _mutable = request.data._mutable

        # set to mutable
        request.data._mutable = True

        # сhange the values you want
        request.data[user_field_name] = value

        # set mutable flag back
        request.data._mutable = _mutable
    return request

class UsersAPIView(generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = UserSerializers

    pagination_class = CustomPagination
  
    queryset = User.objects.all()
    
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('id','username', 'email', 'is_active', 'user_type')



class UserApiView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, username):
        '''
        Helper method to get the object with given  user
        '''
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def get(self, request, username, *args, **kwargs):

        user_instance = self.get_object(username)
        if not user_instance:
            return Response(
                {"res": "الحساب غير موجود"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserSerializers(user_instance)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UpgradeAccountToCustomerApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, UserIsNotCustomer]
    serializer_class = CustomerSerializers

    pagination_class = CustomPagination
  
    queryset = Customer.objects.all()
    
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('id','user','user__username', 'commercial_record', 'location', 'customer_name')

    def post(self, request, *args, **kwargs):

        user = request.user

        user.user_type = '3'

        request = set_request_data(request,request.user.id)



        # if the user have a customer account update account
        try:
            serializer = CustomerSerializers(data=request.data, instance=request.user.customer_account)
        # if not create new customer account
        except:
            serializer = CustomerSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            user.save()
            return Response({'message': 'تمت الترقية بنجاح', 'result': serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        
        instance = self.get_object(request.user.customer_account.id)
        if not instance:
            return Response({"message": "الحساب غير موجود"}, status=status.HTTP_400_BAD_REQUEST)

        request = set_request_data(request,request.user.id)

        serializer = CustomerSerializers(instance=instance,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'تمت تعديل الحساب بنجاح', 'result': serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, id):
        try:
            return Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return None
    



class UpgradeAccountToDriverApiView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, UserIsNotDriver]
    serializer_class = DriverSerializers
    
    pagination_class = CustomPagination

    queryset = Driver.objects.all()
    
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('id', 'user','user__username', 'driver_name', 'car_type', 'car_no', 'location', 'location_type')

    def get_object(self, id):
        try:
            return Driver.objects.get(id=id)
        except Driver.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        user = request.user
        user.user_type = '2'

        request = set_request_data(request,request.user.id)

        serializer = DriverSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user.save()
            return Response({'message': 'تمت الترقية بنجاح', 'result': serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        instance_driver = self.get_object(request.user.driver_account.id)
        if not instance_driver:
            return Response({"message": "الحساب غير موجود"}, status=status.HTTP_400_BAD_REQUEST)

        request = set_request_data(request,request.user.id)

        serializer = DriverSerializers(instance=instance_driver,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'تمت تعديل الحساب بنجاح', 'result': serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


   