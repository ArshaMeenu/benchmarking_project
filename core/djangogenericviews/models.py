from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()
    phone = PhoneNumberField(null=False, blank=False)
    password = models.CharField(max_length=12)
    file = models.FileField(upload_to='documents/')
    image = models.ImageField(upload_to='images/')

    class Meta:
        db_table = "Contact Details"

    def __str__(self):
        return self.name


class ContactFile(models.Model):
    files = models.FileField(upload_to='documents/')
    # contact = models.ForeignKey(Contact, related_name="files",
    #                             on_delete=models.SET_NULL,
    #                             null=True, )

    def __str__(self):
        return self.file
