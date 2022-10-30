from rest_framework import serializers
from account_app.api.serializers import CustomerSerializers, DriverSerializers
from account_app.models import Customer

from services_app.models import Service, Offer, Order

class ServiceSerializers(serializers.ModelSerializer):
    # customer = CustomerDataSerializer(read_only=True) # if user is read only

    class Meta:
        model = Service
        fields = '__all__'

    def to_representation(self, value):
        data = super().to_representation(value)
        data["customer"] = CustomerSerializers(value.customer).data
        return data

    


class OfferSerializers(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'

    def to_representation(self, value):
        data = super().to_representation(value)
        data["driver"] = DriverSerializers(value.driver).data
        data["service"] = ServiceSerializers(value.service).data
        return data

class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, value):
        data = super().to_representation(value)
        data["offer"] = OfferSerializers(value.driver).data
        data["service"] = ServiceSerializers(value.service).data
        return data

