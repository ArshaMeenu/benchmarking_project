from django.db import models


class UID(models.Model):
    rollno = models.IntegerField()



class Student(models.Model):
    uid = models.OneToOneField(UID,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



