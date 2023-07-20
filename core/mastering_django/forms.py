from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.validators import RegexValidator

from .models import Contact, CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


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


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["email","name", "password1", "password2"]
