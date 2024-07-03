from django import forms

class AddressForm(forms.Form):
    street_address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    zip_code = forms.CharField(max_length=10)
    country = forms.CharField(max_length=100)
