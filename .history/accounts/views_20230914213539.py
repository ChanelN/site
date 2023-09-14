from django.contrib.auth import authenticate, login, logout
from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

import django.contrib.auth as auth

#
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from .forms import SignUpForm, LoginForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login
from django.urls import reverse_lazy
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
# again
# parsing data from the client
from rest_framework.parsers import JSONParser
# To bypass having a CSRF token
from django.views.decorators.csrf import csrf_exempt
# for sending response to the client
from django.http import HttpResponse, JsonResponse
# API definition for User
from .serializers import UserSerializer
# model
from .models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from .authentication import CustomUserModelBackend

from .models import User
from . import serializers 
from .serializers import UserSerializer, LoginSerializer

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import views, permissions
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.hashers import check_password, make_password
from . import forms
import requests
import json



#verify whether user is using actual valid gmail account
#the API should be kept in an .env file in my folder for security
api_url = "https://emailvalidation.abstractapi.com/v1/?api_key=7860662ddebe4d90aea328faf185fe5a";
def validate_email(email):
    #request will send email as JSON
    #interpolation for python - str template for js
    response = requests.get(f"{api_url}&email={email}")
    #print(response.content)
    is_valid = is_email_valid(response.content)
    return is_valid
'''
is_valid_email(data):
  if data.is_valid_format.value && is_mx_found && is_smtp_valid:
    if not is_catchall_email && not is_role_email && not is_free_email:
	return true
  return false
'''
def is_email_valid(data):
    data_str = data.decode('utf-8')
    data_dict = json.loads(data_str)
    if data_dict["is_valid_format"]["value"] and data_dict["is_mx_found"]["value"] and data_dict["is_smtp_valid"]["value"]:
        if not data_dict["is_catchall_email"]["value"] and not data_dict["is_role_email"]["value"] and not data_dict["is_free_email"]["value"]:
            return True
    return False

#once user is verified, login() method will take HttpRequest object and user object and save userID in session with django session
#HOME IS MAINPAGEj
def home(request):
    context = {}
    return render(request, "account/home.html", context)
#this viewset will allow us to read,crreate,get,update,delete users
class UserViewset(ModelViewSet):
    #this is the API endpoint that allows users too be viewed or edited
    #authentication_classes = (SessionAuthentication,)
    #permission_classes = (IsAuthenticated,)
    queryset = User.objects.all().order_by('email')
    serializer_class = serializers.UserSerializer
    authenication_classes = []
    permission_classes = []

class SessionView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, format=None):
        return JsonResponse({'isAuthenticated': True})
class WhoAmIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, format=None):
        return JsonResponse({'username': request.user.username})


def get_csrf(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})

#new view for django form consumed by frontend
'''
@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": True, "message": "User registered successfully."})
        else:
            errors = form.errors.as_json()
            return JsonResponse({"success": False, "message": "Error: Invalid form data.", "errors": errors}, status=400)
    else:
        #GET
        form = UserCreationForm()
        return render(request, './templates/registration/signup.html', {'form': form})  
    

def handle_registration(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
#signup
class RegistrationView(views.APIView):
    permission_classes = [permissions.AllowAny,]
    queryset = User.objects.all()

    def post(self, request, format=None):
        #email = request.data.get('email')
        #password = request.data.get('password')
        #dob = request.data.get('dob')
        #MY REQUEST IS A FORM NOT JSON
        email = request.data.get('email')
        is_a_valid_email = validate_email(email)

        if is_a_valid_email:
            serializer = UserSerializer(data=self.request.data)
            if(serializer.is_valid()):
                user = serializer.save()
                return Response({'message': 'Signup success', 'user_id': user.id}, status= status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)
    
#this loginview works with a httpPOST
class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def post(self, request, format=None):
        serializer = serializers.LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        
        if(serializer.is_valid(raise_exception=True)):
            user = serializer.validated_data['user']
            login(request, user)

            csrf_token = get_token(request)
            session_id = request.session.session_key
        
            response_data = {
            'user_id': user.id,
            'username': user.username,
            'csrf_token': csrf_token,
            'session_id': session_id,
            }
            return JsonResponse(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        """
        Parameter: username->user's username who forget old password
        """
        email = request.data.get('email', '')
        users = User.objects.filter(email=email)
        user: User= users[0] if users else None

        if user is not None and user.is_active:
            ret = {'detail': 'User does not exist(Account is incorrect !'}
            return Response(ret, status=403)
    
class LogoutView(views.APIView):
    #serializer_class = serializers.UserSerializer
    #authentication_classes = [CustomUserModelBackend]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        print("im inside of post")
        logout(request) 
        return Response({'detail': 'logout successful !'}, status=status.HTTP_204_NO_CONTENT)

class ProfileUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def put(self,request, *args, **kwargs):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
       
        if 'image' in request.FILES:
            user.image = request.FILES['image']

        current_password = request.data.get("currentPassword")
        new_password = request.data.get("newPassword")
        if current_password and new_password:
            # Check if the current password is correct
            if not user.check_password(current_password):
                return Response(
                    {"error": "Current password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Set the new password
            user.set_password(new_password)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProfileView(generics.RetrieveUpdateAPIView):
    #only to retrieve details, not update
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    '''
    def put(self, request):
        user = request.user  # Assuming you are using session-based authentication
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    '''
#this is just for backend - not accessed by vue
def home(request):
    return render(request, 'account/home.html')

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html')