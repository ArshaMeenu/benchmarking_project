from django.urls import path

from . import views

urlpatterns = [
    path('',views.EmailAttach.as_view(),name ='attach-email')
]