
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import permissions, status
from account_app.api.serializers import UserSerializers

from account_app.models import User


class ApisView(APIView):
    def get(self, request, *args, **kwargs):

        data = {
            'auth':{
                'registration':'http://127.0.0.1:8000/rest-auth/registration/',
                'verify-email':'http://127.0.0.1:8000/rest-auth/registration/verify-email/',
                'account-confirm-email':'http://127.0.0.1:8000/rest-auth/registration/account-confirm-email/<str:key>/',
                'login':'http://127.0.0.1:8000/rest-auth/login/',
                'logout':'http://127.0.0.1:8000/rest-auth/logout/',
                'user':'http://127.0.0.1:8000/rest-auth/user/',
                'password-change':'http://127.0.0.1:8000/rest-auth/password/change/',
            },
            'account':{
                'user-username':'http://127.0.0.1:8000/api/account/users/<str:username>/',
                'users':'http://127.0.0.1:8000/api/account/users/',
                'customer-upgrade':'http://127.0.0.1:8000/api/account/customer-upgrade/',
                'driver-upgrade':'http://127.0.0.1:8000/api/account/driver-upgrade/',
            },
        }

        return Response(data, status=status.HTTP_200_OK)
