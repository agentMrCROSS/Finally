from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('admin/', admin.site.urls),
   path('pages/', include('django.contrib.flatpages.urls')),
   path('news/', include('news.urls')),
   path('', include('news.urls')),
   path('', include('protect.urls')),
   path('sign/', include('sign.urls')),
   path('account/', include('allauth.urls'))
]
