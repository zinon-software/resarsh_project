from rest_framework import serializers

from account_app.models import User, Customer, Driver

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "phone",
        ]

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',"first_name", "last_name", "username", "email",
                  "date_joined", "last_login", "phone", "user_type",
                  "is_admin", "is_active", "is_staff", "is_superuser"
                  ]
        depth = 1


class DriverSerializers(serializers.ModelSerializer):
    #user = UserDataSerializer(read_only=True) # if user is read only
    class Meta:
        model = Driver
        fields = '__all__'

    def to_representation(self, value):
        data = super().to_representation(value)
        data["user"] = UserDataSerializer(value.user).data
        return data


class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
    def to_representation(self, value):
        data = super().to_representation(value)
        data["user"] = UserDataSerializer(value.user).data
        return data

