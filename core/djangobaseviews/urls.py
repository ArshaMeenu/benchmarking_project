from django.urls import path

from .views import *

urlpatterns = [
    path('view/',BaseView.as_view(),name = 'create-read-view'),
    path('delete/<int:id>/', DeleteView.as_view(), name='delete-view'),
    path('edit/<int:pk>/', UpdateView.as_view(), name='edit-view'),

]