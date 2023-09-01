from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.db.models import Q

class ItemManager(models.Manager):
    def get_queryset(self):
        '''
        __ is a lookup filter , gt means greater than. so any endtime greater than crrent time
        '''
        #return super().get_queryset().filter(is_sold=False, end_time__gt=timezone.now())
        return super().get_queryset()
    
    #only items that haven't expire yet
    '''
    def active_items(self):
        #only active items
        now = timezone.now()
        return self.filter(
            Q(end_time__gt=now)| Q(end_time=None),
        ).order_by('end_time')
    '''
    def active_items(self):
        #return self.all().filter(end_time__gt=timezone.now()).order_by('end_time')
        return self.all().order_by('end_time')

    def create_item(self,data):
        '''
        item = self.create(
            title=title,
            description=description,
            starting_price=starting_price,
            end_time=end_time,
            picture=picture,
            category=category,
        )
        '''
        item = self.model(**data)
        item.save()
        return item