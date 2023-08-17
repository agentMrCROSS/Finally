from rest_framework import generics, viewsets
from .models import Pass
from .serializers import Pereval_addedSerializer, PerevalSerializer


def submitData(request):
    data = request.data

    # Проверка наличия необходимых полей
    required_fields = ['beauty_title', 'title', 'other_titles',
                       'connect', 'add_time', 'user', 'coords', 'level', 'images']
    if not all(field in data for field in required_fields):
        return Response({'status': 400, 'message': 'Bad Request', 'id': None})
