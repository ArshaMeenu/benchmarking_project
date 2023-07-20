from django import forms

from .models import BaseViewModel


class BaseViewForm(forms.ModelForm):
    class Meta:
        model = BaseViewModel
        fields = ['title','description']