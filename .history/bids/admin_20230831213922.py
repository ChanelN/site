from django.contrib import admin
from .models import Bid

class CustomBidAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'bidder', 'item', 'bid_price', 'bid_time', 'won')
    list_filter = ('item',) #group by item
    search_fields = ('item', 'creator', 'bidder')

    
admin.site.register(Bid, CustomBidAdmin)