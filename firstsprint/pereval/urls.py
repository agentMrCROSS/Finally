from django.urls import include, path
from rest_framework import routers
from . import views
from .views import CoordinateViewSet, ImageViewSet, UserViewSet, PassViewSet, submitData

router = routers.DefaultRouter()
router.register(r'coordinates', views.CoordinateViewSet)
router.register(r'images', views.ImageViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'passes', views.PassViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('submit-data/', views.submitData, name='submit-data'),
]
