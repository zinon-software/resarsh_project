from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

TYPE = [ 
    ('1','User'),
    ('2','Driver'),
    ('3','Customer'),
]


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=1,choices=TYPE,default='1', null=True, blank=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Account.objects.create(user=instance)
		




class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    driver_name = models.CharField(max_length=200, null=True, blank=True)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200, null=True, blank=True)
