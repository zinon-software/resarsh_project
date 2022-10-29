from django.contrib import admin

from account_app.models import  Customer, Driver, User
from .utility import AccountAdmin
# Register your models here.


admin.site.register(Driver)
admin.site.register(Customer)

admin.site.register(User, AccountAdmin)