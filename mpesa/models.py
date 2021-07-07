from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
# from . import lipanampesa

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.SET_NULL , default=0, blank=True, null=True)
    phone_number = models.CharField(max_length=15,  blank=True, null=True)
    amount = models.FloatField(default=0,  blank=True, null=True)
    time=models.DateTimeField(auto_now_add=True )

    def __str__(self):
        return self.user.username