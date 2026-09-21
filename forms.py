from django import forms
from .models import Assignment


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["title", "description", "due_date", "is_completed", "pdf_file"]


