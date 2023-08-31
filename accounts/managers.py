from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model
#User = get_user_model()


class CustomUserManager(BaseUserManager):
    #cusrom user model manager for user model with unique email as authentication
    #because i removed username, manager needs to use email instead
    #use_in_migrations = True

    def create_user(self, email, dob, password=None, **extra_fields):
        #create and save a user with this email and pass
        if not email:
            raise ValueError('There must be a given email')
        
        #validate email
        email = self.normalize_email(email)
        user = self.model(email=email, dob=dob, **extra_fields)
        user.set_password(password)
        user.save() #using=self._db
        return user


    def create_superuser(self, email, dob, password=None, **extra_fields):
        #creating super user
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must have staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must have superuser=True')

        return self.create_user(email, dob, password, **extra_fields)