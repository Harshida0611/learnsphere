from django.db import models
from quiz.models import Quiz  # Import the Quiz model from the quiz app

class CertificateRequest(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)  # Correct ForeignKey reference
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.quiz.title}"
