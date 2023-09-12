from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.utils import timezone
from .models import Item, User, Bid, Question, Answer

class QuestionViewset(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    authentication_classes = []
    permission_classes = []

class MakeQuestion(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        creator = self.request.data.get('creator')
        try:
            creator = User.objects.get(id=creator)   #try find the user
        except User.DoesNotExist:
            return Response({'message': 'Invalid creator id'}, status=status.HTTP_400_BAD_REQUEST)

        item_id = self.request.data.get('item')
        try:
            item = Item.objects.active_items().get(id=item_id)  # Retrieve the Item instance
        except Item.DoesNotExist:
            return Response({'message': 'Invalid item id'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = serializers.QuestionSerializer(data=request.data)
        if(serializer.is_valid()):
            question = serializer.save(creator=creator, item=item)
            return Response({'message': 'Question submitted', 'question_id': question.id}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)