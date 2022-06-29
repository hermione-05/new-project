from django import forms
from .models import Reviews

class ReviewAdd(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ('review_text','rating')
        widgets ={
            'review_text':forms.Textarea()
        }