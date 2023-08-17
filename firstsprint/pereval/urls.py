from django.urls import path
from .views import Pereval_addedAPICreate


urlpatterns = [
    path('submitData', Pereval_addedAPICreate.as_view()),
]
