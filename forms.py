# forms.py

from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'phone', 'address', 'email', 'password', 'technology', 'photo']
        widgets = {
            'password': forms.PasswordInput(),
        }
