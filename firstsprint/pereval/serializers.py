from .models import *
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class PhotoSerializer(serializers.ModelSerializer):
    # data = serializers.URLField()

    class Meta:
        model = Photo
        # fields = '__all__'
        fields = ['data', 'title']


class Pereval_addedSerializer(WritableNestedModelSerializer):
    photos = PhotoSerializer(many=True)
    user = UserSerializer()
    coords = CoordsSerializer()

    class Meta:
        model = Pereval_added
        fields = '__all__'
        # exclude = ['status']

    def create(self, validated_data):
        photos_data = validated_data.pop('photos', [])
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')

        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        coords_serializer = CoordsSerializer(data=coords_data)
        coords_serializer.is_valid(raise_exception=True)
        coords = coords_serializer.save()

        pereval = Pereval_added.objects.create(user=user, coords=coords, **validated_data)

        # for photo_data in photos_data:
        #     photo_serializer = PhotoSerializer(data=photo_data)
        #     photo_serializer.is_valid(raise_exception=True)
        #     photo = photo_serializer.save(pereval=pereval)

        for photo_data in photos_data:
            data = photo_data.pop('data')
            title = photo_data.pop('title')
            Photo.objects.create(data=data, title=title, pereval=pereval)

        return pereval


# для проверки
class PerevalSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    coords = CoordsSerializer()
    # photo = PhotoSerializer()
    user = UserSerializer()

    class Meta:
        model = Pereval_added
        exclude = ['add_time']
