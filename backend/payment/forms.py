from django import forms
from . models import ShippingAddress

class ShippingForm(forms.ModelForm):
    shipping_full_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}), required=False)
    shipping_email = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}), required=False)
    shipping_city = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=False)
    shipping_county = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'County'}), required=False)
    shipping_address = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}), required=False)


    class Meta:
        model = ShippingAddress
        fields = ["shipping_full_name", "shipping_email", "shipping_city", "shipping_county", "shipping_address"]

        exclude = ["user",]