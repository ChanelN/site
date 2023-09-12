"""
URL configuration for auctionSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
"""
from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.contrib import admin

from accounts.models import User
from accounts.views import UserViewset as Userview
from items.views import ItemViewSet as Itemsview
from bids.views import BidViewset as BidView
from questions.views import QuestionViewset

#added
from rest_framework import routers 
from accounts import views
from django.conf.urls.static import static

#turns out everything is just in the projects urls not indiv apps
#API URLS
#router = routers.DefaultRouter() 
user_router = DefaultRouter()
user_router.register(r'users', Userview)
item_router = DefaultRouter()
item_router.register(r'items', Itemsview)
bid_router = DefaultRouter()
bid_router.register(r'bids', BidView)

#since this is the main projects.url, you link to all the apps from here
urlpatterns = [
    path('', include(user_router.urls)),
    path('', include(item_router.urls)),
    path('', include(bid_router.urls)),
    path('csrf/', views.get_csrf, name='api-csrf'),
    path('api/', include('rest_framework.urls', )),
    path('home/', include('accounts.urls')),
    path('item/', include('items.urls')),
    path('bidding/', include('bids.urls')),
    path('questions/', include('questions.urls')),
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view()),
    path('signup/', views.RegistrationView.as_view()),
    path('profile/', views.ProfileView.as_view()),
    path('profile/<int:id>/', views.ProfileUpdate.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('session/', views.SessionView.as_view(), name='api-session'),  # new
    path('whoami/', views.WhoAmIView.as_view(), name='api-whoami'),  # new
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)