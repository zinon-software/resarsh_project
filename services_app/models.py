from decimal import Decimal
from enum import unique
from django.db import models
from django.urls import reverse

from account_app.models import Customer, Driver, User

# Create your models here.

LOCATION_TYPE = [
    ('1', 'Country To Country'),
    ('2', 'City To City'),
    ('3', 'Inside City'),
]



class Service(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, related_name='customer_service', on_delete=models.CASCADE)
    cargo_info = models.TextField()
    # cargo_images = models.ImageField() # multiple photos
    cargo_type = models.CharField(max_length=50, null=True, blank=True)
    min_price = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))
    max_price = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))
    cargo_weight = models.IntegerField()
    starting_location = models.CharField(max_length=50, null=True, blank=True)
    destination_location = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    location_type = models.CharField(max_length=1, choices=LOCATION_TYPE, default='1', null=True, blank=True)
    created_dt = models.DateTimeField(auto_now_add=True)


class Offer(models.Model):
    driver = models.ForeignKey(Driver, null=True, blank=True, related_name='driver_offer', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, null=True, blank=True, related_name='service_offer', on_delete=models.CASCADE, unique=True)
    message = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))
    created_dt = models.DateTimeField(auto_now_add=True)


ORDER_STATUE = [
    ('accepted', 'مقبول'),
    ('in_progress', 'قيد التنفيذ'),
    ('awaiting_delivery', 'بانتظار التسليم'),
    ('complete', 'مكتمل'),
    ('cancelled', 'ملغي'),
    ('rejected', 'مرفوض'),
]
 

class Order(models.Model):
    # service = models.ForeignKey(Service, null=True, blank=True, related_name='service_order', on_delete=models.CASCADE, unique=True)
    offer = models.ForeignKey(Offer, null=True, blank=True, related_name='offer_order', on_delete=models.CASCADE)
    order_status = models.CharField(max_length=25, choices=ORDER_STATUE, default='accepted', null=True, blank=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    arrival_dt = models.DateTimeField(auto_now=True, null=True, blank=True)
    