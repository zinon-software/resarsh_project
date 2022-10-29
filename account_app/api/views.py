
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import permissions, status
from account_app.api.serializers import UserSerializers

from account_app.models import User


class UserApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, username):
        '''
        Helper method to get the object with given  user
        '''
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def get(self, request, username,*args, **kwargs):

        user_instance = self.get_object(username)
        if not user_instance:
            return Response(
                {"res": "الحساب غير موجود"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = UserSerializers(user_instance)

        return Response(serializer.data, status=status.HTTP_200_OK)
