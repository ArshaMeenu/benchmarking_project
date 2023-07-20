from django.urls import path

from .views import *

urlpatterns = [
    path('onetoone/', OnetoOneRelation, name='onetoone'),
    # path('onetomany/', OnetoOneRelation, name=''),
    # path('manytoone/', OnetoOneRelation, name=''),

]
