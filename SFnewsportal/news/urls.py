from django.urls import path
from .views import PostList, PostDetails, FilterPost, CreatePost, EditPost, DeletePost, CategoryListView, subscribe
from django.views.decorators.cache import cache_page

urlpatterns = [
   path('news/', PostList.as_view(), name='Список новостей'),
   path('<int:pk>', PostDetails.as_view(), name='Просмотр контента'),
   path('search/', FilterPost.as_view(), name='Фильтр контента'),
   path('create/', CreatePost.as_view(), name='Создание новости'),
   path('articles/create/', CreatePost.as_view(), name='Создание статьи'),
   path('articles/<int:pk>/edit/', EditPost.as_view(), name='Изменение статьи'),
   path('<int:pk>/edit/', EditPost.as_view(), name='Изменение новости'),
   path('<int:pk>/delete/', DeletePost.as_view(), name='Удаление новости'),
   path('articles/<int:pk>/delete/', DeletePost.as_view(), name='Удаление статьи'),
   path('categories/<int:pk>/', CategoryListView.as_view(), name='Лист категорий'),
   path('categories/<int:pk>/subscribe/', subscribe, name='Подписка')
]
