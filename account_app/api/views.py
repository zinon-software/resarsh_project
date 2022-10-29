
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import permissions, status
from account_app.api.serializers import DriverSerializers, UserSerializers, CustomerSerializers

from account_app.models import User
from dashboard_app.api.views import ApisView


class UsersAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):

        users = User.objects.all()

        serializer = UserSerializers(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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


class UpgradeAccountToCustomerApiView(ApisView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomerSerializers

    def post(self, request, *args, **kwargs):

        user = request.user

        user.user_type = '3'

        serializer = CustomerSerializers(data=request.data, instance=request.user)

        if serializer.is_valid():
            serializer.save()
            user.save()
            return Response({'message': 'تمت الترقية بنجاح', 'result': serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpgradeAccountToDriverApiView(ApisView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DriverSerializers

    def post(self, request, *args, **kwargs):

        user = request.user
        user.user_type = '2'

        serializer = DriverSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user.save
            return Response({'message': 'تمت الترقية بنجاح', 'result': serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)