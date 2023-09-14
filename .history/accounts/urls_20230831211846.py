'''
maps URLS to views
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
'''
#from mainapp.views import index, books_api, book_api ->the name of the views
#
#
#so the serialiser and router is used together - route to access API
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers 
from accounts import forms
from accounts import views

app_name = 'accounts'
'''
urlpatterns = [
    #path('path name', view used that processes the HTTPrequests, name = "name of view")
    path('login/', LoginView.as_view(), name='userlogin'),
    path('login/home/', LoginView.as_view(), name='login_home'),
    path('home/', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    #
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/home/', home, name='logout_home'),
    path('signup/',SignupView.as_view(), name='usersignup'),
]
'''

urlpatterns = [
    path('', views.home, name='home'),
    path('api-auth', include('rest_framework.urls'), name='login'),
    #
    path('login/', views.LoginView.as_view(), name='userlogin'),
    path('login/home/', views.LoginView.as_view(), name='login_home'),
    path('home/', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    #
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('logout/home/', views.home, name='logout_home'),
    path('signup/',views.RegistrationView.as_view(), name='usersignup'),
]