from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Имя')
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rating_post_author = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum'] * 3
        rating_comm_author = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']
        rating_sum_commPost_author = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rating'))['rating__sum']
        self.rating = rating_post_author + rating_comm_author + rating_sum_commPost_author
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name_category = models.CharField(max_length=50, unique=True, verbose_name='Название категории')
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return self.name_category.title()


class Post(models.Model):
    article = 'ARTICLE'
    news = 'NEWS'
    type_to_choice = [
        (article, 'Статья'),
        (news, 'Новости')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    post_type = models.CharField(max_length=7, choices=type_to_choice, default=news, verbose_name='Вид поста')
    create_data = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=255, verbose_name='Заголовок')
    text_header = models.CharField(max_length=1000, default='Без названия', verbose_name='Контент')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг поста')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text_header[:124] + '...'

    def __str__(self):
        return self.header.title()

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'product-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False, verbose_name='Пользователь')
    text = models.TextField(default='Здесь могла быть ваша реклама!', verbose_name='Комментарий')
    create_data = models.DateTimeField(auto_now_add=True, verbose_name='Дата написания')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг комментария')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
