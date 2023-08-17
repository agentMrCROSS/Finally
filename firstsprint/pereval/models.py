from django.db import models
from .resources import *


class Users(models.Model):
    email = models.EmailField(blank=True)
    phone = models.IntegerField(blank=True)
    name = models.CharField(max_length=255)
    patronimic = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()


class Photo(models.Model):
    data = models.URLField(blank=True, null=True)
    title = models.CharField(max_length=255)
    pereval = models.ForeignKey("Pereval_added", on_delete=models.CASCADE, related_name='photos', blank=True, null=True)


class Pereval_added(models.Model):
    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)

    winter_level = models.CharField(
        max_length=2,
        choices=DIFFICULTY_LEVEL,
        default='1a',
    )
    autumn_level = models.CharField(
        max_length=2,
        choices=DIFFICULTY_LEVEL,
        default='1a',
    )
    spring_level = models.CharField(
        max_length=2,
        choices=DIFFICULTY_LEVEL,
        default='1a',
    )
    summer_level = models.CharField(
        max_length=2,
        choices=DIFFICULTY_LEVEL,
        default='1a',
    )

    status = models.CharField(
        max_length=8,
        choices=STATUS,
        default='NE',
    )

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE, default=None)

