from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView, View
from django.utils import timezone
from .forms import CheckOutForm, PaymentForm
from .models import Item, OrderItem, Order, Billing_Address, Payment
from .keys import phone_number
# Create your views here.


class IndexView(ListView):
    model = Item
    paginate_by = 8
    template_name = 'shop/home-page.html'


class checkoutView(View):
    def get(self, *args, **kwargs):
        form = CheckOutForm()
        context = {
            "form": form
        }
        return render(self.request, 'shop/checkout-page.html', context)

    def post(self, *args, **kwargs):
        form = CheckOutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form, form.cleaned_data.get("street_address")
                apartment_address = form, form.cleaned_data.get(
                    "apartment_address")
                county = form, form.cleaned_data.get("county")
                town = form, form.cleaned_data.get("town")
                zip = form, form.cleaned_data.get("zip")
                # TODO: add functionality to these fields
                # same_shipping_address = form, form.cleaned_data.get(
                #     "same_shipping_address")
                # save_info = form, form.cleaned_data.get("save_info")
                payment_option = form, form.cleaned_data.get(
                    "payment_option")
                billing_address = Billing_Address(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    county=county,
                    town=town,
                    zip=zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # TODO: add a redirect to the selected payment option
                messages.success(self.request, "successfully submitted info")
                return redirect("shop:payment", payment_option)
            messages.warning(self.request, "Failed Process")
            return redirect("shop:checkout-page")
        except ObjectDoesNotExist:
            messages.error(self.request, "you dont have an active cart")
            return redirect("shop:cart")


class PaymentView(View):
    def get(self, *args, **kwargs):
        form = PaymentForm()
        context = {
            "form": form
        }
        return render(self.request, 'shop/payment.html', context)

    def post(self, *args, **kwargs):
        form = PaymentForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                phone_number = form, cleaned_data.get("phone_number")
            Payment.save()
            messages.warning(self.request, "Failed payment Process")
            return redirect("shop:payment")
        except ObjectDoesNotExist:
            messages.error(self.request, "you dont have an active cart")
            return redirect("shop:payment")


class ItemDetailView(DetailView):
    model = Item
    template_name = 'shop/product.html'


class cartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'shop/cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "you dont have an active cart")
            return redirect("/")


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the ordered item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'This Item Quantity Was Updated.')
            return redirect('shop:cart')
        else:
            order.items.add(order_item)
            messages.info(request, 'This Item Was Added To Your Cart.')
            return redirect('shop:cart')

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'This Item Was Added To Your Cart.')
        return redirect('shop:cart')


@ login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # chek if the ordered irem is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, 'This Item Was Removed From Your Cart.')
            return redirect('shop:cart')
        else:
            messages.info(request, 'This Item Was Not In Your Cart.')
            return redirect('shop:product', slug=slug)

    else:
        messages.info(request, 'You Do Not Have an Active Order')
        return redirect('shop:product', slug=slug)


@ login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # chek if the ordered irem is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity != 0:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, 'Item Updated.')
            return redirect('shop:cart')
        else:
            messages.info(request, 'This Item Was Not In Your Cart.')
            return redirect('shop:cart', slug=slug)
    else:
        messages.info(request, 'You Do Not Have an Active Order')
        return redirect('shop:cart', slug=slug)
