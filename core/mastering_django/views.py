import json
import razorpay
from django.views.decorators.csrf import csrf_exempt
from core import settings
from django.contrib import messages
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, FormView, TemplateView, ListView, DetailView, UpdateView, DeleteView
from .constants import PaymentStatus
from .forms import ContactUsForm, RegistrationForm, RegistrationFormSeller2, CartForm
from .models import CustomUser, Product, ProductInCart, Cart, ProductInCart, Order, ProductInOrder
from .tokens import account_activation_token

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

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
        if len(phone) < 10 or len(phone) > 10:  # phone number validation
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
    template_name = 'registerbaseuser.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('mastering_django:signup')

    # def get_success_url(self):  # dynamic url
    #     return reverse_lazy('mastering_django:index-function-view')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user_email = request.POST.get('email')
        if response.status_code == 302:
            user = CustomUser.objects.get(email=user_email)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activate your account"
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user_email
            form = self.get_form()
            try:
                send_mail(
                    subject=mail_subject,
                    message=message,
                    from_email="arsha@sayonetech.com",
                    recipient_list=[to_email, ],
                    fail_silently=False
                    # if it fails due to some error or email id then it get silenced without affecting others
                )
                messages.success(request, 'Check your email for verification link.')
                return self.render_to_response({'form': form})

            except:
                form.add_error('', 'Error occur in sending mail,Try again!')
                messages.error(request, 'Error occur in sending mail,Try again!')
                return self.render_to_response({'form': form})

        else:
            return response


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


# ecommerce online shopping cart project views
class ListProduct(ListView):
    template_name = 'products/listproducts.html'
    model = Product
    context_object_name = 'products'
    # paginate_by = 2
    product_per_page = 2

    def get_context_data(self, **kwargs):
        context = super(ListProduct, self).get_context_data(**kwargs)
        list_product = Product.objects.all()
        product_paginator = Paginator(list_product, self.product_per_page)
        page = self.request.GET.get('page', 1)
        try:
            products = product_paginator.page(page)
        except PageNotAnInteger:
            products = product_paginator.page(1)
        except EmptyPage:
            products = product_paginator.page(product_paginator.num_pages)
        context['products'] = products
        context['is_paginated'] = True
        context['page_obj'] = products
        context['paginator'] = product_paginator
        return context


def sortFilterProducts(request):
    ordering = request.GET.get('ordering', "")  # http://127.0.0.1:8000/listproducts/?page=1&ordering=price
    search = request.GET.get('search', "")
    price = request.GET.get('price', "")
    product_per_page = 2

    if search:
        product = Product.objects.filter(Q(product_name__icontains=search) | Q(
            brand__icontains=search))  # SQLite doesn’t support case-sensitive LIKE statements; contains acts like icontains for SQLite
    else:
        product = Product.objects.all()
    if ordering:
        product = product.order_by(ordering)
    if price:
        product = product.filter(price__lt=price)
    print('product: ', product)

    # Pagination
    page = request.GET.get('page', 1)
    product_paginator = Paginator(product, product_per_page)
    try:
        product = product_paginator.page(page)
    except EmptyPage:
        product = product_paginator.page(product_paginator.num_pages)
    except:
        product = product_paginator.page(product_per_page)
    return render(request, "products/listproducts.html",
                  {"products": product, 'page_obj': product, 'is_paginated': True, 'paginator': product_paginator})


def searchProduct(request):
    if 'term' in request.GET:
        print('term,', request.GET)
        search = request.GET.get('term')
        qs = Product.objects.filter(Q(product_name__icontains=search))[0:10]
        print(list(qs.values()))
        # print(json.dumps(list(qs.values()), cls=DjangoJSONEncoder)) #manually doing jsonresponse here
        titles = list()
        for product in qs:
            titles.append(product.product_name)
        if len(qs) < 10:
            length = 10 - len(qs)
            qs2 = Product.objects.filter(Q(brand__icontains=search))[0:length]
            for product in qs2:
                titles.append(product.brand)
        print(titles)
        return JsonResponse(titles,
                            safe=False)  # [1,2,3,4] ---> "[1,2,3,4]"   queryset ---> serialize into list or dict format ---> json format using json.dumps with a DjangoJSONEncoder(encoder to handle datetime like objects)


class ProductDetail(DetailView):
    model = Product
    template_name = 'products/productdetails.html'
    context_object_name = 'product'


@login_required
def addToCart(request, id):
    try:
        cart = Cart.carts.get(user=request.user)
        try:
            product = Product.objects.get(product_id=id)
            try:
                productincart = ProductInCart.objects.get(cart=cart, product=product)
                productincart.quantity = productincart.quantity + 1
                productincart.save()
                messages.success(request, "Successfully added to cart")
                return redirect(reverse_lazy("mastering_django:display-cart"))
            except:
                productincart = ProductInCart.objects.create(cart=cart, product=product, quantity=1)
                messages.success(request, "Successfully added to cart")
                return redirect(reverse_lazy("mastering_django:display-cart"))
        except:
            messages.error(request, "Product can not be found")
            return redirect(reverse_lazy('mastering_django:list-products'))
    except:
        cart = Cart.carts.create(user=request.user)
        try:
            product = Product.objects.get(product_id=id)
            productincart = ProductInCart.objects.create(cart=cart, product=product, quantity=1)
            messages.success(request, "Successfully added to cart")
            return redirect(reverse_lazy("mastering_django:display-cart"))
        except:
            messages.error(request, "Error in adding to cart. Please try again")
            return redirect(reverse_lazy('mastering_django:list-products'))


class DisplayCart(LoginRequiredMixin, ListView):
    model = ProductInCart
    template_name = "products/displaycart.html"
    context_object_name = "cart"

    def get_queryset(self):
        queryset = ProductInCart.objects.filter(cart=self.request.user.cart)
        return queryset


class UpdateCart(LoginRequiredMixin, UpdateView):
    model = ProductInCart
    form_class = CartForm
    success_url = reverse_lazy('mastering_django:display-cart')

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 302:
            if int(request.POST.get('quantity')) == 0:
                productincart = self.get_object()
                productincart.delete()
            return response
        else:
            messages.error(request, 'error in quantity.')
            return redirect(reverse_lazy('mastering_django:display-cart'))


class DeleteFromCart(LoginRequiredMixin, DeleteView):
    model = ProductInCart
    success_url = reverse_lazy('mastering_django:display-cart')


# Adding Payment Gateway
@login_required
def payment(request):
    if request.method == "POST":
        try:
            cart = Cart.carts.filter(user=request.user)

            products_in_cart = ProductInCart.objects.filter(cart__in=cart)
            final_price = 0
            if (len(products_in_cart) > 0):
                order = Order.objects.create(user=request.user, total_amount=0)
                # order.save()
                for product in products_in_cart:
                    product_in_order = ProductInOrder.objects.create(order=order, product=product.product,
                                                                     quantity=product.quantity,
                                                                     price=product.product.price)
                    final_price = final_price + (product.product.price * product.quantity)
            else:
                return HttpResponse("No product in cart")
        except:
            print()
            return HttpResponse("No product in cart")

        order.total_amount = final_price
        order.save()
        order_currency = 'INR'
        callback_url = 'http://' + str(get_current_site(request)) + "/mastering-django/callback/"
        notes = {'order-type': "basic order from the website", 'key': 'value'}
        razorpay_order = razorpay_client.order.create(
            dict(amount=final_price * 100, currency=order_currency, notes=notes, receipt=order.order_id,
                 payment_capture='0'))
        order.razorpay_order_id = razorpay_order['id']
        order.save()

        return render(request, 'payment/paymentsummaryrazorpay.html',
                      {'order': order, 'razorpay_order_id': razorpay_order['id'], 'orderId': order.order_id,
                       'final_price': final_price, 'razorpay_merchant_id': settings.RAZORPAY_KEY_ID,
                       'callback_url': callback_url})
    else:
        return HttpResponse("505 Not Found")


@csrf_exempt
def callBack(request):  # reference :https://scalereal.com/backend/2021/12/20/razorpay-payment-gateway-integration-with-django.html
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(razorpay_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        print('verify_signature(request.POST)',verify_signature(request.POST))
        if not verify_signature(request.POST):
            order.payment_status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "payment/callback.html", context={"status": order.status})
        else:
            order.payment_status = PaymentStatus.FAILURE
            order.save()
            return render(request, "payment/callback.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.payment_status = PaymentStatus.FAILURE
        order.save()
        return render(request, "payment/callback.html", context={"status": order.status})


# def callBack(request):  # callback view to handle successful and failed payments.
#     if request.method == "POST":
#         try:
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')
#             params_dict = {
#                 'razorpay_order_id': order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }
#             try:
#                 order_db = Order.objects.get(razorpay_order_id=order_id)
#             except:
#                 return HttpResponse("505 Not Found")
#             order_db.razorpay_payment_id = payment_id
#             order_db.razorpay_signature = signature
#             order_db.save()
#             result = razorpay_client.utility.verify_payment_signature(params_dict)
#             print('rslt',result)
#             if result == None:
#                 amount = order_db.total_amount * 100  # we have to pass in paisa
#
#                 try:
#                     razorpay_client.payment.capture(payment_id, amount)
#                     order_db.payment_status = 1
#                     order_db.save()
#                     return render(request, 'payment/paymentsuccess.html', {'id': order_db.id})
#                 except:
#                     order_db.payment_status = 2
#                     order_db.save()
#                     return render(request, 'payment/paymentfailed.html')
#             else:
#
#                 import pdb
#                 pdb.set_trace()
#                 order_db.payment_status = 2
#                 order_db.save()
#                 return render(request, 'payment/paymentfailed.html')
#         except:
#             return HttpResponse("505 not found")
