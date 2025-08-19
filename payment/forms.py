from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
  shipping_full_name= forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}))
  shipping_email= forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))
  shipping_address1= forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address1'}))
  shipping_address2= forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address2'}), required=False)
  shipping_city= forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}))
  shipping_state= forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}), required=False)
  shipping_zipcode= forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zip Code'}), required=False)
  shipping_country= forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}))

  class Meta:
    model=ShippingAddress
    fields=['shipping_full_name','shipping_email','shipping_address1','shipping_address2','shipping_city','shipping_state','shipping_zipcode','shipping_country']
    exclude=['user',]

  
