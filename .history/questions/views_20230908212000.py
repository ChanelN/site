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

#these generics already provide default classes e.g GET, when you're define one, you're creating a custom one
#url = question/ask-question/
class MakeQuestion(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = [IsAuthenticated]
class AnswerQuestion(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        question = self.request.data.get('question_id')

        serializer = serializers.AnswerSerializer(data=request.data)
        if(serializer.is_valid()):
            answer = serializer.save(question_id=question, creator=self.request.user)
            return Response({'message': 'Answered', 'answer_id': answer.id}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-the-url
class itemQuestions(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.QuestionSerializer

    def get_queryset(self):
        item = self.kwargs['id']
        return Question.objects.filter(item=item)
    
class getAnswer(generics.ListAPIView):
    #retrieve list of answers for a specific q id
    permission_classes = [AllowAny]
    serializer_class = serializers.AnswerSerializer

    def get_queryset(self):
        question = self.kwargs['id']
        return Answer.objects.filter(question_id=question)
