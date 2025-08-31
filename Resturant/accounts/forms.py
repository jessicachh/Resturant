from django import forms 
from .models import Profile

class profileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['profile_picture','bio','dob','phone','address']

        widgets={
            'dob':forms.DateInput(attrs={'type':'date'})
        }
    