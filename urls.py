from django.urls import path
from . import views

urlpatterns = [
    path('quiz_list/', views.quiz_list, name='quiz_list'),  # Add this line
    path('<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
]
