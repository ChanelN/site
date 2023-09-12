from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.utils import timezone
from .models import Item, User, Question, Answer

class QuestionViewset(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    authentication_classes = []
    permission_classes = []

#these generics already provide default classes e.g GET, when you define one its a custom one
class MakeQuestion(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = [IsAuthenticated]