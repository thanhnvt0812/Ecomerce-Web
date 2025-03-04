from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
	shipping_full_name = forms.CharField(label="Fullname ", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full Name'}), required=True)
	shipping_email = forms.CharField(label="Email ", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}), required=True)
	shipping_address1 = forms.CharField(label="Address 1 ", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address1'}), required=True)
	shipping_address2 = forms.CharField(label="Address 2", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address2'}), required=False)
	shipping_city = forms.CharField(label="City ", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}), required=True)
	shipping_state = forms.CharField(label="State ", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}), required=False)
	shipping_zipcode = forms.CharField(label="Zipcode ", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}), required=False)
	shipping_country = forms.CharField(label="Country ", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}), required=True)

	class Meta:
		model = ShippingAddress
		fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country']
		exclude = ['user',]

class PaymentForm(forms.Form):
	card_name = forms.CharField(label="Name on Card ", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name on Card'}), required=True)
	card_number = forms.CharField(label="Card Number ", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Number'}), required=True)
	card_exp_date = forms.CharField(label="Expirations Date ", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Expirations Date'}), required=True)
	card_ccv_number = forms.CharField(label="CCV Code ", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'CCV Code'}), required=True)