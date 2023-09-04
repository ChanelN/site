from django.db import models
from accounts.models import User
from items.models import Item
from django.utils import timezone

class Bid(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_item')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids_made')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='bid_item')
    bid_price = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now=True, blank=True)
    won = models.BooleanField(default=False) #this can keep track of whether it is the current highest bid

    objects = models.Manager() 
    
    class Meta:
        permissions = [
            ("can_delete_bid", "can delete bid"),
        ]
    def __str__(self):
        return f"Bid by {self.bidder.email} on {self.item.title} for £{self.bid_price}"