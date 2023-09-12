from django.urls import path, include
from questions import views

urlpatterns = [
    #these views are implemented as classes - inheriting from existing generic view functs
    path('ask-question/', views.MakeQuestion.as_view()),
    path('answer/', views.AnswerQuestion.as_view()),
    path('item-questions/<int:id>/', views.itemQuestions.as_view()),
    path('get-answers/<int:id>/', views.getAnswer.as_view()),
]