from django.contrib import admin

from services_app.models import Offer, Order, Service

# Register your models here.

admin.site.register(Service)
admin.site.register(Offer)
admin.site.register(Order)