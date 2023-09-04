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
'''
class CustomUserModelBackend(BaseAuthentication):
    #allow users to log in with email
    def authenticate(self, request):
        csrf_token = request.META.get('HTTP_X_CSRFTOKEN')
        session_id = request.META.get('HTTP_X_SESSIONID')

        if not csrf_token or not session_id:
            return None
         # Check if the session exists and is not expired
        try:
            session = Session.objects.get(session_key=session_id)
        except Session.DoesNotExist:
            raise AuthenticationFailed('Invalid session ID')

        now = timezone.now()
        if session.expire_date < now:
            raise AuthenticationFailed('Session has expired')

        user_id = session.get_decoded().get('_auth_user_id')
        if user_id:
            try:
                user = CustomUser.objects.get(pk=user_id)
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed('User not found')
        else:
            # If user_id is not present, it means the session is invalid or doesn't have an associated user
            raise AuthenticationFailed('Invalid session')

        return user, None