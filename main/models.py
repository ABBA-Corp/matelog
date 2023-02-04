from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField

# Create your models here.
class CarMarks(models.Model):
    name = models.JSONField('Name', blank=True, null=True)
    image = ThumbnailerImageField(upload_to='car_marks', blank=True, null=True)
    


# cars
class CarsModel(models.Model):
    mark = models.ForeignKey(CarMarks, on_delete=models.CASCADE)
    name = models.CharField("Name", max_length=255)
    year = models.CharField("Год выпуска", blank=True, null=True, max_length=4)
    country = models.CharField('Страна производства', max_length=255, blank=True, null=True)
    image = ThumbnailerImageField(upload_to='cars', blank=True, null=True)
    model = models.CharField('Model', blank=True, null=True, max_length=255)


# 