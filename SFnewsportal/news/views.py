from datetime import datetime

from django.core.cache import cache

from .tasks import send_notification
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from .forms import PostForm
from .models import Post, Category
from .filters import PostFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView
from django.views.decorators.cache import cache_page


class PostList(ListView):
    model = Post
    ordering = '-create_data'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        return context


class PostDetails(DetailView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'product-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'product-{self.kwargs["pk"]}', obj)
            return obj


class FilterPost(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class CreatePost(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post',
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/articles/create/':
            post.post_type = 'A'
        post.save()
        send_notification.delay(post.pk)
        return super().form_valid(form)


class EditPost(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_object(self, **kwargs):
        identification = self.kwargs.get('pk')
        return Post.objects.get(pk=identification)


class DeletePost(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('Список новостей')


class CategoryListView(PostList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_list_news'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-create_data')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@cache_page(60 * 2)
@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы подписались на рассылку новостей из категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})
