from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.validators import RegexValidator

from .models import Contact, CustomUser, Seller, SellerAdditional


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)

# use simple form
# class ContactUsForm(forms.Form):
#     email = forms.EmailField(required=True)
#     name = forms.CharField(max_length=100, required=True)
#     phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number must consist of 10 digits")
#     phone = forms.CharField(max_length=255, required=True, validators=[phone_regex])
#     query = forms.CharField(widget=forms.Textarea)
#     captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

# OR use modelform
class ContactUsForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = Contact
        fields = ['name', 'email', 'query', 'phone', 'captcha']


# class RegistrationFormSeller(UserCreationForm):
#     gst = forms.CharField(max_length=10)
#     warehouse_location = forms.CharField(max_length=1000)
#
#     class Meta:
#         model = Seller
#         fields = ["email","name", "password1", "password2","gst","warehouse_location"]
#


class RegistrationForm(UserCreationForm):
    class Meta:
        model = Seller
        fields = ["email","name", "password1", "password2"]

class RegistrationFormSeller2(forms.ModelForm):
    class Meta:
        model = SellerAdditional
        fields = ['gst','warehouse_location']