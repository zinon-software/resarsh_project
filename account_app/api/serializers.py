from rest_framework import serializers

from account_app.models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email",
                  "date_joined", "last_login", "phone", "user_type",
                  "is_admin", "is_active", "is_staff", "is_superuser"
                  ]
        depth = 1
