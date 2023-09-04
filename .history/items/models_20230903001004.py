from django.db import models
from .managers import ItemManager
from accounts.models import CustomUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import F, Max

class Item(models.Model):
    CATEGORIES = (
        ('LAP', 'Laptop'),
        ('CON', 'Console'),
        ('GAD', 'Gadget'),
        ('GAM', 'Game'),
        ('TEL', 'Tv'),
        ('JWL', 'Jewelry'),
        ('ART', 'Art and collectibles'),
        ('COL', 'Collectibles and memorabilia'),
        ('FAS', 'Fashion & Accessories'),
        ('BKS', 'Books'),
        ('HOM', 'Home or Garden'),
        ('TOY', 'Toys and hobbies'),
    )
    title = models.CharField(max_length=225)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(blank=True, default='item_pictures/no_picture.png', upload_to='item_pictures/')
    end_time = models.DateTimeField()
    date_posted = models.DateTimeField(auto_now=True, blank=True)
    category = models.CharField(
        max_length=3,
        choices=CATEGORIES
    )
    is_sold = models.BooleanField(default=False)
    #Foreignkey to link to user
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_items')

    #objects = models.Manager()  #default
    objects = ItemManager() #custom one

    class Meta:
        permissions = [
                ("can_delete_item", "can delete item"),
        ]

    def __str__(self):
        return self.title
    def is_expired(self):
        return self.end_time <= timezone.now()
    def was_sold(self):
        self.is_sold = True
        self.save()
'''
#django signals
@receiver(pre_save, sender=Item)
def check_expiry(sender, instance, **kwargs):
    #this function connected to 'pre-save' signal
    #is triggered when the item is about to be saved.
    if instance.is_expired() and instance.is_sold:
        instance.delete()
'''