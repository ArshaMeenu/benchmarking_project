import logging

import jwt
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     GenericAPIView, ListAPIView)
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, Plants
from .serializers import (LoginSerializer, PlantSerializer,
                          RegistrationSerializer)
from .verify import send_email, send_otp

logger = logging.getLogger('django')


# landing page view
class DashboardView(APIView):
    def get(self,request):
        try:
            qs = Plants.objects.all()
            return render(request, 'dashboard.html',{'plant_details':qs})
        except  Exception as e:
            logger.error(e,exc_info=True)
            return render(request,template_name='dashboard.html')



# user registration
class RegisterView(APIView):

    def get(self,request):
        return render(request,template_name = 'authentication/register.html')

    def post(self,request,format = None):
        try:

            serializer = RegistrationSerializer(data = request.data)
            serializer.is_valid(raise_exception= True)
            serializer.save()
            return render(request,template_name = 'authentication/login.html')
        except Exception as e:
            return Response(serializer.errors,template_name ='dashboard.html')


# user login view
class LoginView(APIView):

    def get(self, request):
        return render(request, template_name='authentication/login.html')

    def post(self, request, format=None):
        serializer = LoginSerializer(data= request.data)
        serializer.is_valid()
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email = email,password = password)
        request.session['email'] = email
        return redirect("authentication:userprofile")


# LOGOUT
class LogoutView(APIView):
    def get(self,request):
        try:
            logout(request)
            # messages.success(request, 'Successfully logged out', extra_tags='success')
            return redirect("authentication:login")
        except Exception as e:
            logger.error(e,exc_info=True)
            return render(request,status=status.HTTP_204_NO_CONTENT,template_name=None)



# userprofile
class UserProfileView(APIView):
    def get(self,request):
        print('userprofile started')
        user = CustomUser.objects.filter(email = request.session['email']).values('username','email','user_image').first()
        context = {
            'username':user['username'],
            'email':user['email'],
            'userimage':user['user_image']
        }
        return render(request,context = context,template_name='authentication/userprofile.html' )



# Create Plant by a user
class UserCreatePlants(APIView):
    def post(self,request):
        try:
            data = request.data #fetch plants data
            serializer = PlantSerializer(data = data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return render(request,template_name='authentication/userprofile.html' )
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, status=status.HTTP_204_NO_CONTENT, template_name=None)


# View more details of each plant:
class PlantDetailView(APIView):
    def get(self,request,pk):
        try:
            plant_data = Plants.objects.filter(id = pk).values().first()
            serialized = PlantSerializer(plant_data)
            context = {
                'data' : serialized.data
            }
            return render(request,template_name='plants/plant_detail.html',context=context)
            # return redirect('authentication:userprofile')
        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, status=status.HTTP_204_NO_CONTENT, template_name=None)



class FavoritePlantView(ListAPIView):
    def get(self,request,*args, **kwargs):
        try:
            obj_id = self.kwargs.get('pk')
            data = Plants.objects.filter(pk=obj_id).first()
            serialize = PlantSerializer(data)
            context = {
                'data': serialize.data
            }
            return render(request,template_name='plants/favorite_plant_details.html',context=context)

        except Exception as e:
            logger.error(e, exc_info=True)
            return render(request, status=status.HTTP_204_NO_CONTENT, template_name=None)





# Add to Card section

class AddToCartPlantView(ListAPIView):
    serializer_class = PlantSerializer
    queryset = serializer_class.Meta.model
    def get(self,request,*args, **kwargs):
        print('start')
        obj_id = self.kwargs.get('pk')
        print('id',obj_id)
        # queryset = self.queryset.objects.filter(id = id)
        # print('qry',queryset)
        data = Plants.objects.filter(pk=obj_id).first()
        serialized = PlantSerializer(data)
        context = {
            'data': serialized.data
        }
        print('serialized',serialized.data)

        return render(self.request,template_name='plants/plant_to_card.html',context=context)




# delete plant

# class DeletePlantView(DestroyAPIView):
#     serializer_class = PlantSerializer
#     lookup_field = 'id'
#
#     def delete(self, request, *args, **kwargs):
#         # id = request.GET.get('id', '')
#         plant = get_object_or_404(Plants, pk=self.kwargs.get('pk'))
#         print('plant',plant)
#         return render(request,template_name='plants/favorite_plant_details.html')

    # def get_queryset(self):
    #     print('delete')
    #     id = self.request.GET.get('id', '')
    #     print('id',self.request)
    #
    #     return Plants.objects.filter(id = id)
    # def delete(self, request,pk,format=None):
    #     print('dlee')
    #     plant = Plants.objects.filter(id = pk)
    #     print(plant,'plant')
    #     return Response('hai')





# class DestroyPlantView(DestroyAPIView):
#     serializer_class = PlantSerializer
#     queryset = Plants.objects.all()
#     def perform_destroy(self, instance):
#         instance.delete_flag = True
#         instance.save()
#



    # serializer_class = PlantSerializer
    # def destroy(self, request, *args, **kwargs):
    #     print('deleted')
    #     instance = self.get_object()
    #     self.perform_destroy(instance)'



    # def delete(self, request, *args, **kwargs):
    #     print('deleted')
    #     plant = get_object_or_404(Plants, pk=kwargs['pk'])
    #
    #     # plant = self.get_object(pk)
    #     plant.delete()
    #     return redirect("authentication:favorite_plant_details")

