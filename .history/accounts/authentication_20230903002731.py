# app.backends.py

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.sessions.models import Session
from django.utils import timezone


from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
#SO THIS IS THE CUSTOM AUTHENTICATION BACKEND FOR THE CUSTOM USER
'''
I have to use this custom authentication class instead of built in one because of 
different domains for front and backend -

'''
CustomUser = get_user_model()

class CustomUserModelBackend(BaseBackend):
    #allow users to log in with email
    def authenticate(self, request, email=None, password=None, **kwargs):
        # You can use the 'username' parameter to pass the email for authentication.
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None  # No user with this email address.

        # Check the user's password (you might want to use Django's built-in password verification here).
        if user.check_password(password):
            return user  # Authentication successful.
        else:
            return None  # Incorrect password.

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None