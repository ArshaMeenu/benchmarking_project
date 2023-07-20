from django import forms


class EmailForm(forms.Form):
    email = forms.EmailField()
    attach = forms.ImageField(widget=forms.ClearableFileInput())    # for multiple attachments.
    # attach = forms.FileField()
    message = forms.CharField(widget=forms.Textarea)