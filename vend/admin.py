from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _

from .models import Vendor

class VendorInline(admin.StackedInline):
    model = Vendor

class AccountsUserAdmin(UserAdmin):
    inlines = (VendorInline, )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

def vendor_name(obj):
    return obj.user.get_full_name()

def vendor_email(obj):
    return obj.user.username

vendor_name.short_description = 'Vendor Name'
vendor_email.short_description = 'Vendor Email'

class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', vendor_name, vendor_email, 'phone_number')

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(User, AccountsUserAdmin)