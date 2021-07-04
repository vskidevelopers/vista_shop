from django.contrib import admin
from .models import Item, Order, OrderItem, Billing_Address, Payment
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']


admin.site.register(Item)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Payment)
