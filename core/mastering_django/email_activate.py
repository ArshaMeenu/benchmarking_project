from django.contrib.auth import login
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from mastering_django.models import CustomUser
from mastering_django.tokens import account_activation_token


def activate(request, uidb64, token):
    try:
        print('email')
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        # messages.success(request, "Successfully logged in.")
        # return redirect(reverse_lazy('mastering_django:index-function-view'))
    else:
        return HttpResponse('Activation link is invalid or your account is already verified .Try to Login.')
