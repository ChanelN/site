from django.contrib import admin
from .models import Question, Answer

class CustomQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'question', 'item', 'date', 'answered')
    list_filter = ('item',)
    search_fields = ('item', 'creator', )

class CustomAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_id', 'creator', 'answer', 'date' )
    list_filter = ('question_id',)
    search_fields = ('question_id', 'creator', )

admin.site.register(Question, CustomQuestionAdmin)
admin.site.register(Answer, CustomAnswerAdmin)
