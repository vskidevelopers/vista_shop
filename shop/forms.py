from django import forms

PAYMENT_CHOICES = (
    # ('S', 'Stripe'),
    # ('P', 'Paypal'),
    ('M', 'Mpesa'),
)


class CheckOutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234 Main St',
        'class': 'form-control'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or suite',
        'class': 'form-control'
    }))
    county = forms.CharField()
    town = forms.CharField()
    zip = forms.CharField()
    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_options = forms.ChoiceField(
        widget=forms.RadioSelect, choices=(PAYMENT_CHOICES))


class PaymentForm(forms.Form):
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Eg: 25412345678',
        'class': 'custom-control-input'
    }))
