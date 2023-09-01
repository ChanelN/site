from django.contrib import admin
from .models import Item

class CustomItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'title', 'description', 'starting_price', 'end_time', 'category', 'is_sold')
    list_filter = ('category', 'is_sold')
    
# Register your models here.
admin.site.register(Item, CustomItemAdmin)