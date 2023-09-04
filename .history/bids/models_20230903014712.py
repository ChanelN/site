from django.db import models
from items.models import Item
'''
class Bid(models.Model):
    #i can't have both foreign keys pointing to the CustomUser to be on_delete=models.CASCADE due to integrity issues
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_item')
    bidder = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='bids_made')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='bid_item')
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now=True, blank=True)
    won = models.BooleanField(default=False) #this can keep track of whether it is the current highest bid

    objects = models.Manager() 
    
    class Meta:
        permissions = [
            ("can_delete_bid", "can delete bid"),
            ("can_change_bid", "Can change bid"),
        ]
    def __str__(self):
        return f"Bid by {self.bidder.email} on {self.item.title} for £{self.bid_price}"
'''
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.sessions.models import Session
from django.utils import timezone

from .models import CustomUser
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