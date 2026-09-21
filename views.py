from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Quiz

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz})
