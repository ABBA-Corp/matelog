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

    def __str__(self):
        try:
            lng = Languages.objects.filter(default=True).first()
            name = self.name.get(lng.code, '')
            mark = self.mark.name.get(lng.code, '')

            return f'{mark} {name}'
        except:
            return 'Car'


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
    distance = models.CharField('Distance', max_length=255)
    date = models.DateField()
    vehicle = models.ForeignKey(CarsModel, on_delete=models.CASCADE)
    ship_from = models.ForeignKey(City, on_delete=models.CASCADE, related_name='ship_from_order')
    ship_to = models.ForeignKey(City, on_delete=models.CASCADE, related_name='ship_to_orders')
    vehicle_runs = models.CharField('Vehicle Runs', max_length=255, choices=VEHICLE_RUNS)
    ship_via_id = models.CharField('Ship via id', max_length=255, choices=SHIP_VIA_ID)
    price = models.FloatField('Price', validators=[MinValueValidator(1)], blank=True, null=True)
    price_first_tarif = models.FloatField('Price', validators=[MinValueValidator(1)], blank=True, null=True)
    price_second_tarif = models.FloatField('Price', validators=[MinValueValidator(1)], blank=True, null=True)
    email = models.EmailField('Email')
    nbm = models.CharField('Nbm', blank=True, null=True, max_length=255)
    car_year = models.CharField("Car year", max_length=4, validators=[is_numeric_validator])
    #service_type = models.ForeignKey()

    def format_date(self):
        return f'{self.date.month}/{self.date.day}/{self.date.year}'


# application
class Applications(models.Model):
    VEHICLE_RUNS = [('1', 'Yes'), ('0', 'No')]
    SHIP_VIA_ID = [('1', 'Open'), ('2', 'Enclosed')]
    TARIFS = [('1', '500$ tarif'), ('2', '200$ tarif')]
    SHIP_TYPES = [('An individual', 'An individual'), ('General', 'General')]
    STATUS = [('Accepted', 'Accepted'), ('Delivered', 'Delivered'), ('Canseled', 'Canseled')]
    ADRES_TYPES = [('Residentional adress', 'Residentional adress'), ('Business adress', 'Business adress')]

    distance = models.CharField('Distance', max_length=255, blank=True, null=True)
    date = models.DateField()  # it
    vehicle = models.ForeignKey(CarsModel, on_delete=models.CASCADE)  # it
    ship_from = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name='ship_fromappl')  # it
    ship_to = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name='ship_to_appl')  # it
    vehicle_runs = models.CharField(
        'Vehicle Runs', max_length=255, choices=VEHICLE_RUNS)
    ship_via_id = models.CharField(
        'Ship via id', max_length=255, choices=SHIP_VIA_ID)
    price = models.FloatField('Price', validators=[MinValueValidator(1)], blank=True, null=True)  # it
    tarif = models.CharField('Tarif', max_length=255, choices=TARIFS)
    email = models.EmailField('Email')
    ship_type = models.CharField('Ship type', max_length=255, choices=SHIP_TYPES)
    first_name = models.CharField('first name', max_length=255)
    last_name = models.CharField('last name', max_length=255)
    car_year = models.CharField("Car year", max_length=4, validators=[is_numeric_validator], blank=True, null=True)
    status = models.CharField("Status", max_length=255, choices=STATUS, default='Accepted')  # this
    adres = models.CharField('Adres', max_length=255)
    deckription = models.TextField('Deskription', blank=True, null=True)
    admin_notes = models.TextField('Notes', blank=True, null=True)
    final_price = models.FloatField('Final Price', validators=[MinValueValidator(1)], blank=True, null=True)
    contact_me = models.BooleanField('Contact me', default=True)
    contact_else = models.CharField('Contact else', blank=True, null=True, max_length=10, validators=[is_numeric_validator])
    adres_type = models.CharField("Adres type", max_length=255, choices=ADRES_TYPES)


    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_format_date(self):
        return str(self.date.year) + '-' + str(self.date.month) + '-' + str(self.date.day)


# application nbm
class AplicationNbm(models.Model):
    application = models.ForeignKey(Applications, on_delete=models.CASCADE, related_name='nbms')
    nbm = models.CharField('Nbm', blank=True, null=True, max_length=10, validators=[is_numeric_validator])



# short applications
class ShortApplication(models.Model):
    STATUS = [('На рассмотрении', "На рассмотрении"), ("Рассмотрено", "Рассмотрено"), ("Отклонено", "Отклонено")]

    nbm = models.CharField('Nbm', max_length=10, validators=[is_numeric_validator])
    status = models.CharField('Status', default='На рассмотрении', max_length=255, choices=STATUS)



# short apl
class SomeAplication(models.Model):
    SUBJECT = [('0', 'I want a free quote'), ('1', 'I have an existing order'),
               ('2', 'I want to book a shipment'), ('3', 'Other questions')]

    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField('Email', blank=True, null=True) 
    nmb = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField('Subject', max_length=255, choices=SUBJECT, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)


