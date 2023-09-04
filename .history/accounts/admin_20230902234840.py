from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.contrib.auth.models import Group
from .forms import CustomUserChangeForm, SignUpForm
from .models import CustomUser

# Register your models here to show them on adminsa

class CustomUserAdmin(BaseUserAdmin):
    #allows you to change these fields in admin module

    #these forms to add and change user instances
    add_form = SignUpForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('id', 'email', 'dob', 'is_staff', 'is_active')
    list_filter= ('email','is_active')
    fieldsets = (
        (None, {'fields': ('email','password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'dob','image', 'bio')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'dob', 'password1', 'password2')}
        ),
    )
    #fields to display the User model in admin site, override base UserAdmin
    
    ordering = ('email',)
    search_fields =('email',)
    filter_horizontal = ()

#register new userAdmin
admin.site.register(CustomUser, CustomUserAdmin)
#unregister Group model as we;re not using django permissions