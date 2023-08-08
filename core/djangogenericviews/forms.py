from django import forms
from django.contrib.auth import password_validation
from django.core import validators
from multiupload.fields import MultiFileField, MultiImageField
from phonenumber_field.formfields import PhoneNumberField

from .models import Contact


class ContactForm(forms.ModelForm):
    # password = forms.CharField(label='Password', widget=forms.PasswordInput,
    #                            help_text=password_validation.password_validators_help_text_html)
    # confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    # file = MultiFileField(min_num=1, max_num=10, max_file_size=1024 * 1024 * 5) #for multiple file selection
    file = forms.FileField(required=False,
                           widget=forms.ClearableFileInput(attrs={'name': 'contact_image', 'allow_multiple_selected': True}))
    image = MultiImageField(min_num=1, max_num=3, max_file_size=1024 * 1024 * 5)

    class Meta:
        model = Contact
        # fields = [ 'name','address', 'email', 'phone', 'password', 'confirm_password', 'files', 'image']
        fields = "__all__"
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = self.cleaned_data['password']
    #     confirm_password = self.cleaned_data['confirm_password']
    #
    #     if password != confirm_password:
    #         raise forms.ValidationError("doesn't match")
    #     password_validation.validate_password(self.cleaned_data.get('password', None))
    #     return self.cleaned_data
