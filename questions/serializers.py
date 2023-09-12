from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Item, User, Question, Answer

class QuestionSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    creator_readable = serializers.StringRelatedField(source='creator', read_only=True) #human readable rep

    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), write_only=True)
    item_readable = serializers.StringRelatedField(source='item', read_only=True)

    class Meta:
        model = Question
        fields = '__all__'
        #fields = ['creator', 'creator_readable', 'question', 'item', 'item_readable', 'date', 'answered']

class AnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), write_only=True)
    question_readable = serializers.StringRelatedField(source='question_id', read_only=True) #human readable rep

    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    creator_readable = serializers.StringRelatedField(source='creator', read_only=True) #human readable rep

    class Meta:
        model = Answer
        fields = ['question_id', 'question_readable', 'creator', 'creator_readable', 'answer', 'date']