from django.urls import path, include
from questions import views

urlpatterns = [
    path('ask-question/', views.MakeQuestion.as_view()),
    path('item-questions/<int:id>/', views.itemQuestions.as_view()),
]