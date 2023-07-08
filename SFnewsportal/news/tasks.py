import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news.models import Post, Category
from celery import shared_task


@shared_task
def send_notification(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    title = post.header
    subscribers_emails = []
    for category in categories:
        subscribers_users = category.subscribers.all()
        for user in subscribers_users:
            subscribers_emails.append(user.email)

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': post.preview,
            'link': f'{settings.SITE_URL}/news/{pk}',

        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    print('Уведомление отправлено подписчику')


@shared_task
def action_every_monday_8am():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(create_data__gte=last_week)
    categories = set(posts.values_list('category__name_category', flat=True))
    subscribers = set(Category.objects.filter(name_category__in=categories).values_list('subscribers__email', flat=True))

    html_context = render_to_string(
        'daily_post.html',
        {'link': settings.SITE_URL,
         'posts': posts
         }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()
    print('Еженедельное оповещение отправлено!')
