from django.urls import include, path

from . import views

urlpatterns = [
    path('index-function-view/', views.indexfunctionview, name="index-function-view"),
    path('index-class-view/', views.IndexClassView.as_view(), name="index-class-view"),
    path('contactus/', views.contactus, name="contact-us"),
    path('contactus2/', views.contactus2, name="contact-us"),
    path('contactus-class-view/', views.ContactUs.as_view(), name="contactus-class-view"),
    # authentication endpoints
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginViewUser.as_view(), name='login'),
    path('signup-seller/', views.RegisterViewSeller.as_view(), name='signup-seller'),
    path('logout/', views.LogoutViewUser.as_view(), name='logout'),

]
