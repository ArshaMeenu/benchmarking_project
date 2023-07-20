from django.urls import path

from .views import *

urlpatterns =[
    path('list-view/',ContactListView.as_view(),name = 'list-view'),
    path('detail-view/<int:pk>/', ContactDetailView.as_view(), name='detail-view'),
    path('create-view/', ContactCreateView.as_view(), name='create-view'),
    path('update-view/<int:pk>/', ContactUpdateView.as_view(), name='update-view'),
    path('delete-view/<int:pk>/', ContactDeleteView.as_view(), name='delete-view'),
    path('form-view/', ContactFormView.as_view(),name = 'form-view'),
    path('template-view/', ContactTemplateView.as_view(), name='template-view'),

]