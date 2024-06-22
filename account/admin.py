from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from account.models import Account
from .models import Item, Order, OrderItem, Address

class AccountAdmin(UserAdmin):
    model = Account
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login')
    

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class ItemAdminModel(admin.ModelAdmin):
    search_fields = ['name']
    prepopulated_fields = {'slug': ('title', )}
    list_display = [
        'title',
        'category',
        'price',
        'quantity',
        'digital',
        'image',
        'description',
        
    ]

class AddressAdminModel(admin.ModelAdmin):
    list_display = [
        'street_address',
        'apartment_address',
        'country',
        'zip',
        'default',
        
    ]

admin.site.register(Account, AccountAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Item, ItemAdminModel)
admin.site.register(Address, AddressAdminModel)



