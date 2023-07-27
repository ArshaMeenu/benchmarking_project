from django.urls import include, path

from . import views,email_activate

urlpatterns = [
    path('index-function-view/', views.indexfunctionview, name="index-function-view"),
    path('index-class-view/', views.IndexClassView.as_view(), name="index-class-view"),
    path('contactus/', views.contactus, name="contact-us"),
    path('contactus2/', views.contactus2, name="contact-us"),
    path('contactus-class-view/', views.ContactUs.as_view(), name="contactus-class-view"),
    # authentication endpoints
    path('signup/', views.RegisterView.as_view(), name='signup'),
    path('login/', views.LoginViewUser.as_view(), name='login'),
    path('signup-seller/', views.RegisterViewSeller.as_view(), name='signup-seller'),
    path('logout/', views.LogoutViewUser.as_view(), name='logout'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         email_activate.activate, name='activate'),

]
