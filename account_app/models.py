from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from account_app.utility import MyAccountManager

# Create your models here.

TYPE = [
    ('1', 'User'),
    ('2', 'Driver'),
    ('3', 'Customer'),
]


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$", message="الرقم غير صحيح برجاء ادخال رقم صحيح")
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True, null=True, blank=True)
    user_type = models.CharField(max_length=1, choices=TYPE, default='1', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        pass
        # print("is created")
        # Token.objects.create(user=instance)
        # Profile.objects.create(user=instance)

        # # متابعة الادمن
        # current_user = instance
        # other_user = Account.objects.get(pk=1)
        # current_user.profile.follows.add(other_user)
        # other_user.profile.followers.add(current_user)


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    driver_name = models.CharField(max_length=200, null=True, blank=True)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200, null=True, blank=True)
