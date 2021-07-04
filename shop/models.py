from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

# from .lipanampesa import lipa_na_mpesa
# Create your models here.

CATEGORY_CHOICES = (
    ('H', 'Hedsets'),
    ('E', 'Earphones'),
    ('M', 'Mouse'),
    ('C', 'Cables'),
    ('K', 'Keyboard')
)

LABEL_CHOICES = (
    ('D', 'danger'),
    ('P', 'primary'),
    ('S', 'secondary'),
    ('SS', 'success')
)


class Item(models.Model):
    title = models.CharField(max_length=128)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=2)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to='images', height_field=None,
                                width_field=None, max_length=None,  null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shop:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("shop:add_to_cart", kwargs={
            'slug': self.slug
        })

    def remove_from_cart_url(self):
        return reverse("shop:remove_from_cart", kwargs={
            'slug': self.slug
        })

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amaount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    Billing_address = models.ForeignKey(
        "Billing_Address", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class Billing_Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
