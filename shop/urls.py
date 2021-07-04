from django.urls import path
from .views import (
    checkoutView,
    PaymentView,
    ItemDetailView,
    add_to_cart, remove_from_cart,
    IndexView,
    cartView,
    remove_single_item_from_cart
)

app_name = 'shop'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('checkout/', checkoutView.as_view(), name='checkout-page'),
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cartView.as_view(), name='cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('remove_single_item_from_cart/<slug>/', remove_single_item_from_cart, name='remove_single_item_from_cart'),
]
