from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView, CreateView

from django.contrib.auth.views import LoginView, LogoutView
from .forms import ContactUsForm, RegistrationForm, RegistrationFormSeller2
from .models import SellerAdditional, CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin


# function based view
def indexfunctionview(request):
    age = 10
    arr = ['asr', 888, 'poa', 'flapjack', 887]
    dic = {'a': 1, 'b': 'oak'}
    return render(request, 'index.html', {
        'age': age, 'arr': arr, 'dic': dic
    })
    # return HttpResponse('<h1>hello</h1>')


# class based view
class IndexClassView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        age = 10,
        arr = ['asr', 888, 'poa', 'flapjack', 887],
        dic = {'a': 1, 'b': 'oak'}
        context_old = super().get_context_data(**kwargs)
        context = {
            'age': age, 'arr': arr, 'dic': dic, 'context_old': context_old
        }
        return context


# normal way of form data
def contactus(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST['phone']
        if len(phone) < 10 or len(phone) > 10: # phone number validation
            # return HttpResponse('error in entry')
            raise ValidationError('phone number length is not right')
        query = request.POST['query']
        print(name + '' + email + '' + phone + '' + query)
    return render(request, 'contactus.html')


# function based custom forms
def contactus2(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            if len(form.cleaned_data.get('query')) > 10:
                form.add_error('query', 'query length is not right')
                return render(request, 'contactus2.html', {'form': form})
            form.save()

            return HttpResponse('Success')
        else:
            if len(form.cleaned_data.get('query')) > 10:
                form.add_error('query', 'query length is not right')
                # form.errors['query'] = 'Query length is not right.'
            return render(request, 'contactus2.html', {'form': form})

    return render(request, 'contactus2.html', {'form': ContactUsForm})


# class based for forms
class ContactUs(FormView):
    form_class = ContactUsForm
    template_name = 'contactus2.html'
    # success_url = '/index-function-view' #hardcoded url

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        if len(form.cleaned_data.get('query')) > 10:
            form.add_error('query', 'query length is not right')
            return render(self.request, 'contactus2.html', {'form': form})
        form.save()
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        if len(form.cleaned_data.get('query')) > 10:
            form.add_error('query', 'query length is not right')
            # form.errors['query'] = 'Query length is not right.'
        response = super().form_invalid(form)
        return response

    def get_success_url(self):  # dynamic url
        return reverse('mastering_django:index-function-view')


# class RegisterViewSeller(CreateView):
#     template_name = 'register.html'
#     form_class = RegistrationFormSeller
#     # success_url = reverse('mastering_django:index-function-view')
#
#     def get_success_url(self): #dynamic url
#         return reverse_lazy('mastering_django:index-function-view')
#
#     # override the post
#     def post(self,request,*args,**kwargs):
#         response = super().post(request,*args,**kwargs)
#         if response.status_code ==302:
#             gst = request.POST.get('gst')
#             warehouse_location = request.POST.get('warehouse_location')
#             user = CustomUser.objects.get(email = request.POST.get('email'))
#             s_add = SellerAdditional.objects.create(user = user, gst = gst, warehouse_location = warehouse_location)
#             return response
#         else:
#             return response

class RegisterView(CreateView):
    template_name = 'registerbasicuser.html'
    form_class = RegistrationForm
    # success_url = reverse('mastering_django:index-function-view')

    def get_success_url(self):  # dynamic url
        return reverse_lazy('mastering_django:index-function-view')


class LoginViewUser(LoginView):
    template_name = "login.html"


class RegisterViewSeller(LoginRequiredMixin, CreateView):
    template_name = 'registerseller.html'
    form_class = RegistrationFormSeller2
    success_url = reverse_lazy('mastering_django:index-function-view')

    def form_valid(self, form):
        user = self.request.user
        user.type.append(user.Types.SELLER)
        user.save()
        form.instance.user = self.request.user
        return super().form_valid(form)


class LogoutViewUser(LogoutView):
    success_url = reverse_lazy('mastering_django:index-function-view')

