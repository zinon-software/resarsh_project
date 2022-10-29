from django.contrib import admin

from account_app.models import Account, Customer, Driver

# Register your models here.
admin.site.register(Account)
admin.site.register(Driver)
admin.site.register(Customer)