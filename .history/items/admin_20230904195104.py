from django.contrib import admin
from .models import Item

class CustomItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'title', 'description', 'starting_price', 'end_time', 'category')
    list_filter = ('category')
    
# Register your models here.
admin.site.register(Item, CustomItemAdmin)