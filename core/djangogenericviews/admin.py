from django.contrib import admin

from .models import Contact, ContactFile

admin.site.register(Contact)
admin.site.register(ContactFile)