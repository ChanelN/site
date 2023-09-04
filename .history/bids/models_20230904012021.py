from django.db import models
from accounts.models import User
from items.models import Item
from django.utils import timezone

class Bid(models.Model):
    #i need to delete user and revert won=True
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
            ("can_change_bid", "Can change bid"),
        ]

    def set_as_won(self):
        # Find the previously highest bidder who is not the current bidder
        previous_highest_bidder = Bid.objects.filter(
            creator=self.creator,
            won=True
        ).exclude(bidder=self.bidder).first()

        if previous_highest_bidder:
            previous_highest_bidder.won = True
            previous_highest_bidder.save()
    def delete(self, using=None, keep_parents=False):
        # Check if the bidder being deleted is the current highest bidder
        if self.won:
            # Update the previously highest bidder as the winner
            self.set_as_won()
        super().delete(using, keep_parents)

    def __str__(self):
        return f"Bid by {self.bidder.email} on {self.item.title} for £{self.bid_price}"
    