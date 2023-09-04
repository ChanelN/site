from django.urls import path, include
from items import views

#the beginning is item e.g item/add-item/
urlpatterns =[
    path('add-item/', views.AddItem.as_view()),
    path('update/<int:id>/', views.UpdateItem.as_view()),
    path('auctionItems/', views.ViewUserItems.as_view()),
    path('activeItems/', views.ViewActiveItems.as_view()),
    path('expiredItems/', views.ViewExpiredItems.as_view()),
    path('soldItems/', views.ViewSoldItems.as_view()),
    path('delete/<int:id>/', views.deleteItem.as_view()),
    path('highest-bid/<int:id>/', views.highestBid.as_view()),
    path('category/<str:cat>/', views.categoryItems.as_view()),
]