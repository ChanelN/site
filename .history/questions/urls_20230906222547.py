from django.urls import path, include
from questions import views

urlpatterns = [
    path('ask-question/', views.MakeQuestion.as_view()),
]
