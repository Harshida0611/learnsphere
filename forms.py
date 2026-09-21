from django import forms
from .models import Quiz, Question

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'due_date']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'text', 'option1', 'option2', 'option3', 'option4', 'correct_option']
