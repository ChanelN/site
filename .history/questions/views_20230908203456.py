from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.sessions.models import Session
from .models import Item, User, Question, Answer
#starts with question/

class QuestionViewset(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    authentication_classes = []
    permission_classes = []

#these generics already provide default classes e.g GET, when you define one its a custom one
#url = question/ask-question/
class MakeQuestion(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = [IsAuthenticated]

#https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-the-url
class itemQuestions(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.QuestionSerializer

    def get_queryset(self):
        item = self.kwargs['id']
        return Question.objects.filter(item=item)