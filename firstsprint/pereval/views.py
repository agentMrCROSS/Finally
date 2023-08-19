from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from .models import Coordinate, Image, User, Pass
from .serializers import CoordinateSerializer, ImageSerializer, UserSerializer, PassSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response


class CoordinateViewSet(viewsets.ModelViewSet):
    queryset = Coordinate.objects.all()
    serializer_class = CoordinateSerializer

    @swagger_auto_schema(operation_description="Get the list of coordinates")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new coordinate")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Retrieve a coordinate by ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Update a coordinate by ID")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Delete a coordinate by ID")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    @swagger_auto_schema(operation_description="Get the list of images")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new image")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Retrieve an image by ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Update an image by ID")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Delete an image by ID")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(operation_description="Get the list of users")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new user")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Retrieve a user by ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Update a user by ID")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Delete a user by ID")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PassViewSet(viewsets.ModelViewSet):
    queryset = Pass.objects.all()
    serializer_class = PassSerializer

    @swagger_auto_schema(operation_description="Get the list of passes")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Create a new pass")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Retrieve a pass by ID")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Update a pass by ID")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Delete a pass by ID")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@swagger_auto_schema(method='POST', operation_description="Submit data")
@api_view(['POST'])
def submitData(request):
    data = request.data

    # Проверка наличия необходимых полей
    required_fields = ['beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'user', 'coords', 'level',
                       'images']
    if not all(field in data for field in required_fields):
        return Response({'status': 400, 'message': 'Bad Request', 'id': None})

    try:
        # Сериализация и сохранение данных
        coordinate_data = data['coords']
        coordinate_serializer = CoordinateSerializer(data=coordinate_data)
        if not coordinate_serializer.is_valid():
            return Response({'status': 400, 'message': 'Invalid coordinate data', 'id': None})
        coordinate = coordinate_serializer.save()

        user_data = data['user']
        user_serializer = UserSerializer(data=user_data)
        if not user_serializer.is_valid():
            return Response({'status': 400, 'message': 'Invalid user data', 'id': None})
        user = user_serializer.save()

        # Проверка поля level
        level_data = data.get('level')
        if level_data is None:
            return Response({'status': 400, 'message': 'Field "level" is required', 'id': None})

        # Проверка наличия обязательных подполей в поле level
        required_level_fields = ['winter', 'summer', 'autumn', 'spring']
        if not all(field in level_data for field in required_level_fields):
            return Response({'status': 400, 'message': 'Missing required fields in "level"', 'id': None})

        # Дополнительные проверки формата или значений подполей в поле level
        if not all(isinstance(level_data[field], str) for field in required_level_fields):
            return Response({'status': 400, 'message': 'Invalid format in "level"', 'id': None})

        pass_data = {
            'beauty_title': data['beauty_title'],
            'title': data['title'],
            'other_titles': data['other_titles'],
            'connect': data['connect'],
            'add_time': data['add_time'],
            'user': user.id,
            'coords': coordinate.id,
            'level': level_data,
        }
        pass_serializer = PassSerializer(data=pass_data)
        if not pass_serializer.is_valid():
            return Response({'status': 400, 'message': 'Invalid pass data', 'id': None})
        pass_object = pass_serializer.save()

        # Проверка поля images
        images_data = data.get('images')
        if images_data is None:
            return Response({'status': 400, 'message': 'Field "images" is required', 'id': None})

        # Проверка наличия обязательных подполей в поле images
        required_image_fields = ['data', 'title']
        for image_data in images_data:
            if not all(field in image_data for field in required_image_fields):
                return Response({'status': 400, 'message': 'Missing required fields in "images"', 'id': None})

            # Дополнительные проверки формата или значений подполей в поле images
            if not isinstance(image_data['data'], str) or not isinstance(image_data['title'], str):
                return Response({'status': 400, 'message': 'Invalid format in "images"', 'id': None})

            image_data['pass'] = pass_object.id
            image_serializer = ImageSerializer(data=image_data)
            if not image_serializer.is_valid():
                return Response({'status': 400, 'message': 'Invalid image data', 'id': None})
            image_serializer.save()

        # Установка значения поля status в "new"
        pass_object.status = "new"
        pass_object.save()
        print(f"New pass object created with status: {pass_object.status}")

        return Response({'status': 200, 'message': 'Data submitted successfully', 'id': pass_object.id})

    except (ValidationError, Exception) as e:
        return Response({'status': 500, 'message': str(e), 'id': None})


@swagger_auto_schema(method='GET')
@api_view(['GET'])
def get_pass_by_id(request, id):
    try:
        # Получение объекта перевала по его id
        pass_object = Pass.objects.get(id=id)
        serializer = PassSerializer(pass_object)
        return Response(serializer.data)
    except Pass.DoesNotExist:
        return Response({'status': 404, 'message': 'Pass not found', 'id': None})


@swagger_auto_schema(method='PATCH')
@api_view(['PATCH'])
def editData(request, id):
    try:
        # Проверяем, существует ли объект с указанным id
        pass_object = Pass.objects.get(pk=id)

        # Проверяем, что объект находится в статусе "new"
        if pass_object.status != "new":
            return Response({'state': 0, 'message': 'The pass cannot be edited as it is not in "new" status.'})

        # Проверяем, что переданные данные валидны
        pass_serializer = PassSerializer(data=request.data, instance=pass_object, partial=True)
        if not pass_serializer.is_valid():
            return Response({'state': 0, 'message': 'Invalid pass data', 'errors': pass_serializer.errors})

        # Сохраняем отредактированные данные
        pass_serializer.save()

        return Response({'state': 1, 'message': 'Pass data updated successfully'})

    except Pass.DoesNotExist:
        return Response({'state': 0, 'message': 'Pass object not found'})


@swagger_auto_schema(method='GET')
@api_view(['GET'])
def getPassesByUserEmail(request):
    email = request.GET.get('user__email')
    if not email:
        return Response({'message': 'Email parameter is required.'}, status=400)

    passes = Pass.objects.filter(user__email=email)
    pass_serializer = PassSerializer(passes, many=True)

    return Response(pass_serializer.data)
