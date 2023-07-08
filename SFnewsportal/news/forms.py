from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'category', 'header', 'text_header']

    def clean(self):
        cleaned_data = super().clean()
        header = cleaned_data.get('header')
        text_header = cleaned_data.get('text_header')
        if header == text_header:
            raise ValidationError('Заголовок идентичен тексту контента')
        return cleaned_data
