from django.contrib import admin

from account_app.models import Account, Customer, Driver, User
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Account)
admin.site.register(Driver)
admin.site.register(Customer)


class AccountAdmin(UserAdmin):
    list_display = ('email','username','date_joined', 'last_login', 'is_admin','is_staff')
    search_fields = ('email','username',)
    readonly_fields=('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, AccountAdmin)