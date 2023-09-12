from django.db import models
from accounts.models import User
from items.models import Item

class Question(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_user')
    question = models.TextField(max_length=250, unique=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='question_subject')
    date = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default=False)

    def __str__(self):
        return self.question
    
class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_user')
    answer = models.TextField(max_length=1000, unique=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer