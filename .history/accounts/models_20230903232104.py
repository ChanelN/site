from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
import datetime
# Create your models here.

from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model
from .managers import CustomUserManager
'''m
referencing the custom user model:
e.g class profile(models.Model):
user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
#other fields

user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
'''
class User(AbstractUser):
    #set auth_user_model to this

    username = None #so we dont get the username property from the AbstractUser
    email = models.EmailField(max_length=254, unique=True)
    '''
    made email field required
    USERNAME_FIELD defines the unique identifier for the users,makes user login with it
    REQUIRED_FIELDS are what theyre prompted for when you create a user, in AbstractUser email is part of this
    all objects for the class come from the custom user manager
    '''

    image = models.ImageField(blank=True, default = 'UserDefault.jpeg') #Image field for profile picture
    dob = models.DateField(null=False, default = datetime.date.today)
    bio = models.TextField(max_length=250, default="This is my bio!", unique=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD ='email' #email of user will be returned from get_email_field_name()
    REQUIRED_FIELDS = ['dob'] #no other aditional fields required

    class Meta:
        permissions = [
            ("can_delete_user", "can delete user"),
            ("can_change_customuser", "Can change CustomUser"),
        ]

    def to_dict(self):
        """return dictionary of object"""
        return {
            'id': self.id,
            'email': self.email,
            'dob': self.dob,
            'image': self.image,
            'bio': self.bio,
        }

    objects = CustomUserManager()
    def __str__(self):
        return self.email