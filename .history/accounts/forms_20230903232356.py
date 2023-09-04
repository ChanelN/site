#accounts/forms.py
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

#i can create forms here and consume it on the frontend - therefore
#these forms replace the default behaviour allowed on admin site
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    dob = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta(UserCreationForm.Meta):
        model=User
        fields=['email', 'dob']
 
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        #fields = ['id', 'email', ]

class LoginForm(forms.Form):
    #this will validate login data sent to the API
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

'''
#user creation form is a built in django register form
class SignUpForm(forms.ModelForm):
    #password1 = forms.CharField(widget=forms.PasswordInput)
    #password2 = forms.CharField(label='confirm password', widget= forms.PasswordInput)
    email = forms.EmailField(max_length=200)
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def verify_email(self):
        #check email is available
        email = self.cleaned_data.get('email')
        otherAccount = User.objects.filter(email=email)
        if otherAccount.exists():
            raise forms.ValidationError("email is taken")
        return email

    def verify_passwords(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 is not None and password1!=password2:
            self.add_error("password2", "your passwords dont match")
        return cleaned_data

    def save(self, commit=True):
        #save password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user
class LoginForm(forms.ModelForm):
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ["email", "password"]

    #define errors
    def clean(self):
        if self.is_valid():
            email=self.cleaned_data.get("email")
            password = self.cleaned_data.get("password")
            if not authenticate(username=email, password=password):
                raise forms.ValidationError("invalid login")

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_staff','is_active')
'''