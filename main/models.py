from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from admins.models import telephone_validator
from django.core.exceptions import ValidationError
import uuid


def is_numeric_validator(value):
    if str(value).isnumeric() is False:
        raise ValidationError(
            ("Your telephone number is invalid"),
            params={'value': value}
        )



# Create your models here.
class CarMarks(models.Model):
    name = models.JSONField('Name', blank=True, null=True)
    


# cars
class CarsModel(models.Model):
    VEHICLE_TYPES = [('Car', 'Car'), ('SUV', 'SUV'), ('Pickup', 'Pickup')]

    mark = models.ForeignKey(CarMarks, on_delete=models.CASCADE, related_name='cars')
    name = models.JSONField("Name", blank=True, null=True, max_length=255)
    vehicle_type = models.CharField('Vehicle type', max_length=255, choices=VEHICLE_TYPES, default='Car')


# states
class States(models.Model):
    name = models.JSONField('State name', blank=True, null=True)
    code = models.CharField('State code', max_length=255)


# cities
class City(models.Model):
    name = models.JSONField('Name', blank=True, null=True)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    zip = models.CharField('City zip', max_length=255, unique=True)
    text = models.JSONField('Text', blank=True, null=True)



# lead
class Leads(models.Model):
    VEHICLE_RUNS = [('Yes', '1'), ('No', '0')]
    SHIP_VIA_ID = [('Open', '1'), ('Enclosed', '2')]

    uuid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    distance = models.PositiveIntegerField('Distance', blank=True, null=True)
    date = models.DateField()
    vehicle = models.ForeignKey(CarsModel, on_delete=models.CASCADE)
    ship_from = models.ForeignKey(City, on_delete=models.CASCADE, related_name='ship_from_order')
    ship_to = models.ForeignKey(City, on_delete=models.CASCADE, related_name='ship_to_orders')
    vehicle_runs = models.CharField('Vehicle Runs', max_length=255, choices=VEHICLE_RUNS)
    ship_via_id = models.CharField('Ship via id', max_length=255, choices=SHIP_VIA_ID)
    price = models.FloatField('Price', validators=[MinValueValidator(1)])
    email = models.EmailField('Email')
    nbm = models.CharField('Nbm', blank=True, null=True, max_length=10, validators=[is_numeric_validator])
    #service_type = models.ForeignKey()