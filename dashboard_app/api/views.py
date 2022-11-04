
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import permissions, status
from account_app.api.serializers import UserSerializers

from account_app.models import User


class ApisView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, *args, **kwargs):

        buseUrl = 'http://127.0.0.1:8000/'

        data = {
            'auth':{
                'registration': buseUrl + 'api/auth/registration/',
                'verify-email': buseUrl + 'api/auth/registration/verify-email/',
                'account-confirm-email': buseUrl + 'api/auth/registration/account-confirm-email/<str:key>/',
                'login': buseUrl + 'api/auth/login/',
                'logout': buseUrl + 'api-auth/logout/',
                'user': buseUrl + 'api/auth/user/',
                'password-change': buseUrl + 'api/auth/password/change/',
            },
            'account':{
                'user-username': buseUrl + 'api/account/users/<str:username>/',
                'users': buseUrl + 'api/account/users/',
                'customer-upgrade': buseUrl + 'api/account/customer-upgrade/',
                'driver-upgrade': buseUrl + 'api/account/driver-upgrade/',
            },
            'service':{
                'services': buseUrl + 'api/services/',
                'service': buseUrl + 'api/services/<srt:service>/',
                'my-services': buseUrl + 'api/my-services/',
                'offers': buseUrl + 'api/offers/',
                'offer': buseUrl + 'api/offers/<str:offer>',
                'orders': buseUrl + 'api/orders/',
                'order': buseUrl + 'api/orders/<str:order>',
            },
        }

        return Response(data, status=status.HTTP_200_OK)
