from django.db import models


class User(models.Model):
    email = models.EmailField()
    fam = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    otc = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)


class Coordinate(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()


class Image(models.Model):
    data = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=255)


class Pass(models.Model):
    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.TextField(blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.ForeignKey(Coordinate, on_delete=models.CASCADE)
    level = models.JSONField(default=dict, blank=True)
    images = models.ManyToManyField(Image)
    status = models.CharField(max_length=255, choices=(
        ('new', 'New'),
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ))

    def create_pass(self, pass_data):
        # Создание новой записи перевала
        pass_object = self.create(**pass_data)
        # Установка значения поля status в "new"
        pass_object.status = "new"
        pass_object.save()
        return pass_object
