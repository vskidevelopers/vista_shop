from django.contrib import admin
from .models import Item, Order, OrderItem, Billing_Address, Category


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']

class Billing_AddressAdmin(admin.ModelAdmin):
    list_display=['user', 'street_address', 'apartment_address','county','town','zip']

admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Billing_Address, Billing_AddressAdmin)
admin.site.register(Category)

