from django.urls import path, include
from items import views
from bids import views

#the beginning is bidding e.g. bidding/place-bid
urlpatterns =[
    path('place-bid/', views.MakeBid.as_view(), name="place-bid"),
    path('update/<int:id>/', view.UpdateBid.as_view()),
]