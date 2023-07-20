from django.urls import path

from .views import *

urlpatterns = [
    path('complex-query/',ComplexQuery.as_view(),name= 'complex-query')
]