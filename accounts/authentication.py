# app.backends.py

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.sessions.models import Session
from django.utils import timezone

from .models import CustomUser
#SO THIS IS THE CUSTOM AUTHENTICATION BACKEND FOR THE CUSTOM USER
'''
I have to use this custom authentication class instead of built in one because of 
different domains for front and backend -

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