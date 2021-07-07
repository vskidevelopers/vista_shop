from django.contrib import admin
from .models import Payment
# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user","phone_number","amount", "time")

admin.site.register(Payment, PaymentAdmin)