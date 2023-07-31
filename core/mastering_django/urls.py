from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views, email_activate

urlpatterns = [
    path('index-function-view/', views.indexfunctionview, name="index-function-view"),
    path('', views.IndexClassView.as_view(), name="index-class-view"),
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

    # change password
    path('password_change/',auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html',success_url=reverse_lazy("mastering_django:password_change_done")),name='password_change'),
    path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='registration/passwordchange_done.html'),name='password_change_done'),

    # Forgot/Reset password
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html",
                                              success_url=reverse_lazy("mastering_django:password_reset_done"),
                                              email_template_name='registration/forgot_password_email.html'),
                                              name="reset_password"),  # 1
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"),
                                              name="password_reset_done"),  # 2
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="registration/passwordreset_form.html",
                                              success_url=reverse_lazy("mastering_django:password_reset_complete")),
                                              name="password_reset_confirm"),  # 3
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="registration/passwordreset_done.html"),
                                             name="password_reset_complete"),  # 4
]
