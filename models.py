from django.db import models

class AssignmentSubmission(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    pdf_file = models.FileField(upload_to='assignments/')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
