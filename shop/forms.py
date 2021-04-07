from django import forms
from django_countries.fields import CountryField

class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : "1234 Main St" 
                        }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder' : "1234 Main St" 
                        }))
    country = CountryField(blank_label='(select country)').formfield()
    pin = forms.CharField()
    same_billing_address = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    save_info = forms.BooleanField(required=False, widget=forms.CheckboxInput())

