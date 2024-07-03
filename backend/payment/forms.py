from django import forms
from . models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}), required=False)
    shipping_email = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}), required=False)
    shipping_city = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=False)
    shipping_county = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'County'}), required=False)
    shipping_address = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}), required=False)

    shipping_latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    shipping_longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)


    class Meta:
        model = ShippingAddress
        fields = ["shipping_full_name", "shipping_email", "shipping_city", "shipping_county", "shipping_address", "shipping_latitude", "shipping_longitude"]

        exclude = ["user",]


class PaymentForm(forms.Form):
    card_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name On Card'}), required=False)
    card_number = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Number'}), required=False)
    card_exp_date = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Expiration Date'}), required=False)
    card_cvv_number = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'CVV Number'}), required=False)
    card_address = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Address'}), required=False)
    card_city = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card City'}), required=False)
    card_country = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card County'}), required=False)




