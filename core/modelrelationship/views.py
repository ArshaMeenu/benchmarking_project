from django.shortcuts import HttpResponse, render
from django.views import *
from django.views.generic import View

from .models import *


def OnetoOneRelation(request):
    uid = UID.objects.filter(id=1)
    print('uid', uid)
    student = Student.objects.get(uid=uid)
    print('s', student)
    return HttpResponse('student')
