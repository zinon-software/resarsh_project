from rest_framework import serializers

from services_app.models import Service, Offer, Order



class ServiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class OfferSerializers(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'
        depth = 1

class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        depth = 1

