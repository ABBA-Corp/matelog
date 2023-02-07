from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from admins.models import telephone_validator
from django.core.exceptions import ValidationError
import uuid
from admins.models import Languages

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

    def get_name(self):
        lng = Languages.objects.filter(default=True).first()
        name = self.name.get(lng.code, '')
        mark = self.mark.name.get(lng.code, '')

        return f'{mark} {name}'

# states
class States(models.Model):
    name = models.JSONField('State name', blank=True, null=True)
    code = models.CharField('State code', max_length=255)


# cities
class City(models.Model):
    name = models.JSONField('Name', blank=True, null=True)
    state = models.ForeignKey(States, on_delete=models.CASCADE)
    zip = models.CharField('City zip', max_length=5, unique=True)
    text = models.JSONField('Text', blank=True, null=True)



# lead
class Leads(models.Model):
    VEHICLE_RUNS = [('1', 'Yes'), ('0', 'No')]
    SHIP_VIA_ID = [('1', '1'), ('2', '2')]

    uuid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    distance = models.PositiveIntegerField('Distance', blank=True, null=True)
    date = models.DateField()
    vehicle = models.ForeignKey(CarsModel, on_delete=models.CASCADE)
    ship_from = models.ForeignKey(City, on_delete=models.CASCADE, related_name='ship_from_order')
    ship_to = models.ForeignKey(City, on_delete=models.CASCADE, related_name='ship_to_orders')
    vehicle_runs = models.CharField('Vehicle Runs', max_length=255, choices=VEHICLE_RUNS)
    ship_via_id = models.CharField('Ship via id', max_length=255, choices=SHIP_VIA_ID)
    price_first_tarif = models.FloatField('Price', validators=[MinValueValidator(1)], blank=True, null=True)
    price_second_tarif = models.FloatField('Price', validators=[MinValueValidator(1)], blank=True, null=True)
    email = models.EmailField('Email')
    nbm = models.CharField('Nbm', blank=True, null=True, max_length=10, validators=[is_numeric_validator])
    #service_type = models.ForeignKey()


    def format_date(self):
        return f'{self.date.month}/{self.date.day}/{self.date.year}'




# application
class Applications(models.Model):
    VEHICLE_RUNS = [('1', 'Yes'), ('0', 'No')]
    SHIP_VIA_ID = [('1', '1'), ('2', '2')]
    TARIFS = [('1', '1'), ('2', '2')]
    SHIP_TYPES = [('An individual', 'An individual'), ('General', 'General')]
    STATUS = [('Accepted', 'Accepted'), ('Delivered', 'Delivered')]


    distance = models.PositiveIntegerField('Distance', blank=True, null=True) # imortant
    date = models.DateField() # it
    vehicle = models.ForeignKey(CarsModel, on_delete=models.CASCADE) # it
    ship_from = models.ForeignKey(City, on_delete=models.CASCADE, related_name='ship_fromappl') # it
    ship_to = models.ForeignKey(City, on_delete=models.CASCADE, related_name='ship_to_appl') # it
    vehicle_runs = models.CharField('Vehicle Runs', max_length=255, choices=VEHICLE_RUNS)
    ship_via_id = models.CharField('Ship via id', max_length=255, choices=SHIP_VIA_ID)
    price = models.FloatField('Price', validators=[MinValueValidator(1)], blank=True, null=True) # it
    tarif = models.CharField('Tarif', max_length=255, choices=TARIFS)
    email = models.EmailField('Email') 
    ship_type = models.CharField('Ship type', max_length=255, choices=SHIP_TYPES)
    first_name = models.CharField('first name', max_length=255)
    last_name = models.CharField('last name', max_length=255)
    status = models.CharField("Status", max_length=255, choices=STATUS, default='Accepted') # this


    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_price(self):
        price = self.price
        if not self.price:
            price = 0
        

        if self.tarif == '1':
            return price + 200
        elif self.tarif == "2":
            return price + 500

    



# application nbm
class AplicationNbm(models.Model):
    application = models.ForeignKey(Applications, on_delete=models.CASCADE, related_name='nbms')
    nbm = models.CharField('Nbm', blank=True, null=True, max_length=10, validators=[is_numeric_validator])



