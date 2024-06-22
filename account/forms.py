from account.models import Item
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.forms import ModelForm, fields, widgets
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField

from account.models import Account, USERTYPE_CHOICES


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')
    usertype  = forms.ChoiceField(choices= USERTYPE_CHOICES, required=True)
    class Meta:
        model = Account
        fields = ("email", "username", "password1", "password2", "usertype",)
       

        def save(self, commit=True):
            user = super(UserCreationForm, self).save(commit=False)
            user.usertype = self.cleaned_data["usertype"]
            if commit:
                user.save()
            return user



class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('username', 'password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Invalid login")


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal'),
)

class AddressForm(forms.Form):
    street_address = forms.CharField()
    apartment_address = forms.CharField()
    country = CountryField().formfield(widget=CountrySelectWidget(attrs={
        "class":"custom-select d-block w-100"
    }))
    zip = forms.CharField()
    save_info = forms.BooleanField(required=False)
    default = forms.BooleanField(required=False)   
    use_default = forms.BooleanField(required=False)
    payment_choice = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)
