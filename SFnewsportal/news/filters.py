import django_filters
from django_filters import FilterSet
from .models import Post, Author
from django import forms


class PostFilter(FilterSet):

    author = django_filters.ModelChoiceFilter(field_name='author',
                                              label='Выбор автора',
                                              lookup_expr='exact',
                                              queryset=Author.objects.all())
    date = django_filters.DateFilter(field_name='create_data',
                                     widget=forms.DateInput(attrs={'type': 'date'}), label='Позже указанной даты',
                                     lookup_expr='gt')
    header = django_filters.ModelChoiceFilter(field_name='header',
                                              label='Поиск по названию',
                                              lookup_expr='icontains',
                                              queryset=Post.objects.all())
