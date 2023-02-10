from rest_framework import serializers
from admins.models import Services, Articles, ArticleImages, StaticInformation, AboutUs, Languages, Translations, MetaTags, Reviews
from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from .models import CarMarks, CarsModel, City, States, Leads, Applications, AplicationNbm, ShortApplication
from django.conf import settings
import requests

class ThumbnailSerializer(serializers.ImageField):
    def __init__(self, alias, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alias = alias

    def to_representation(self, instance):
        url = thumbnail_url(instance, self.alias)

        if url == '':
            return None

        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)


        return url


# field lang serializer
class JsonFieldSerializer(serializers.Serializer): 
    def to_representation(self, instance):
        language = self.context['request'].headers.get('Language')

        if not language:
            language = Languages.objects.filter(default=True).first().code

        data = instance.get(language)
        
        return data


# meta serializer
class MetaFieldSerializer(serializers.ModelSerializer):
    meta_keys = JsonFieldSerializer()
    meta_deck = JsonFieldSerializer()

    class Meta:
        model = MetaTags
        exclude = ['id']



# articles
class ArticleSerializer(serializers.ModelSerializer):
    title = JsonFieldSerializer()
    subtitle = JsonFieldSerializer()
    body = JsonFieldSerializer()
    created_date = serializers.DateField(format="%Y.%m.%d")
    image = ThumbnailSerializer(alias='prod_photo')
    author = serializers.ReadOnlyField(source='author.username')
    meta = MetaFieldSerializer()

    class Meta:
        model = Articles
        fields = '__all__'



# service serializer
class ServiceSerializer(serializers.ModelSerializer):
    title = JsonFieldSerializer()
    sub_title = JsonFieldSerializer()
    deckription = JsonFieldSerializer()
    image = ThumbnailSerializer(alias='prod_photo')
    meta_field = MetaFieldSerializer()

    class Meta:
        model = Services
        fields = "__all__"



# about us
class AboutUsSerializer(serializers.ModelSerializer):
    title_one = JsonFieldSerializer()
    title_second = JsonFieldSerializer()
    text_first = JsonFieldSerializer()
    text_second = JsonFieldSerializer()

    class Meta:
        model = AboutUs
        exclude = ['id']


# static information
class StaticInformationSerializer(serializers.ModelSerializer):
    title = JsonFieldSerializer()
    subtitle = JsonFieldSerializer()
    deskription = JsonFieldSerializer()
    about_us = JsonFieldSerializer()
    adres = JsonFieldSerializer()
    work_time = JsonFieldSerializer()
    logo_first = ThumbnailSerializer(alias='prod_photo')
    logo_second = ThumbnailSerializer(alias='prod_photo')

    class Meta:
        model = StaticInformation
        exclude = ['id']



# translation serializer
class TranslationSerializer(serializers.Serializer):
    def to_representation(self, instance):          
        data = {}

        for item in instance:
            language = self.context['request'].headers.get('Language')

            if not language:
                language = Languages.objects.filter(default=True).first().code
            
            val = item.value.get(language, '')
            key = str(item.group.sub_text) + '.' + str(item.key)
            data[key] = val

        return data




# langs serializer
class LangsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        fields = '__all__'



# car mark serializer
class CarMarkSerializer(serializers.ModelSerializer):
    name = JsonFieldSerializer()

    class Meta:
        model = CarMarks
        fields = "__all__"



# car model serializer
class CarModelSerializer(serializers.ModelSerializer):
    mark = CarMarkSerializer()
    name = JsonFieldSerializer()

    class Meta:
        model = CarsModel
        fields = '__all__'


# state serializer
class StateSerializer(serializers.ModelSerializer):
    name = JsonFieldSerializer()
    class Meta:
        model = States
        fields = '__all__'


# get city coordinates by zip
def get_coordinates(city):
    coord_params = {
        "zip": city.zip,
        "key": "17o8dysaCDrgvlc"
    }

    coord_request = requests.get('https://api.promaptools.com/service/us/zip-lat-lng/get/', params=coord_params).json()
    lat = coord_request.get("output")[0].get('latitude')
    lon = coord_request.get("output")[0].get("longitude")

    return (lat, lon)


# city serializer
class CitySerializer(serializers.ModelSerializer):
    name = JsonFieldSerializer()
    text = JsonFieldSerializer()
    state = StateSerializer()

    class Meta:
        model = City
        fields = "__all__"


    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        params = {
            "zip": instance.zip,
            "key": "17o8dysaCDrgvlc"
        }

        coord_request = get_coordinates(instance)

        iframe = f"""<iframe width="100%" height="300" allowfullscreen="allowfullscreen" loading="lazy" referrerpolicy="no-referrer-when-downgrade" style="border: 0px;" class="lazyLoad isLoaded" src="https://maps.google.com/maps?q={ coord_request[0] },{ coord_request[1] }&hl=es&z=14&amp;output=embed"></iframe>"""
        data['iframe'] = iframe

        return data


# city simple srializer
class CitySimpleSerializer(serializers.ModelSerializer):
    name = JsonFieldSerializer()
    text = JsonFieldSerializer()
    state = StateSerializer()

    class Meta:
        model = City
        fields = "__all__"




# lead view serializer
class LeadsViewSerializer(serializers.ModelSerializer):
    ship_from = CitySerializer()
    ship_to = CitySerializer()
    vehicle = CarModelSerializer()

    class Meta:
        model = Leads
        fields = "__all__"


# lead serializer
class LeadsCreateSerialzier(serializers.ModelSerializer):
    distance = serializers.IntegerField(required=False)

    class Meta:
        model = Leads
        fields = '__all__'
        read_only_fields = ['price', 'price_first_tarif ', 'price_second_tarif']


    
    def save(self, **kwargs):
        lead = super().save(**kwargs)
        url = 'https://ml.msgplane.com/api/rest/get/price/'

        params = {
            'api_key': settings.SRM_API_KEY,
            "pickup_zip": lead.ship_from.zip,
            "dropoff_zip": lead.ship_to.zip,
            "estimated_ship_date": str(lead.format_date()),
            "vehicle_type": lead.vehicle.vehicle_type,
            "ship_via_id": lead.ship_via_id,
            "vehicle_runs": lead.vehicle_runs
        }
        price_request = requests.get(url=url, params=params).json()

        if not price_request:
            price_request = {}

        lead.price = float(price_request.get('1', 0))
        lead.price_first_tarif = float(price_request.get('1', 0)) + 200
        lead.price_second_tarif = float(price_request.get('1', 0)) + 500

        point_a = get_coordinates(lead.ship_to)
        point_b = get_coordinates(lead.ship_from)

        lead.save()
        
        return lead

    def to_representation(self, instance):
        serializer = LeadsViewSerializer(instance, context={'request': self.context.get('request')})

        return serializer.data
        


# application nbm serializer
class ApplicationNbmSerializer(serializers.ModelSerializer):
    class Meta:
        model = AplicationNbm
        exclude = ['application']


# aplication serializer
class AplicationViewSerializer(serializers.ModelSerializer):
    vehicle = CarModelSerializer()
    ship_from = CitySimpleSerializer()
    ship_to = CitySerializer()
    nbms = ApplicationNbmSerializer()
    
    class Meta:
        model = Applications
        fields = '__all__'


# aplication create serializer
class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applications
        fields = '__all__'
        extra_kwargs = {
            'price': {"required": False},
            'distance': {"required": False},
            'ship_from': {"required": False},
            'ship_to': {"required": False},
            'vehicle': {"required": False},
            'date': {"required": False},
            'vehicle_runs': {"required": False},
            'ship_via_id': {"required": False},
            'email': {"required": False}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        lead_id = request.data.get('lead')
        lead = Leads.objects.get(id=lead_id)

        validated_data['distance'] = lead.distance
        validated_data['ship_from'] = lead.ship_from
        validated_data['ship_to'] = lead.ship_to
        validated_data['vehicle'] = lead.vehicle
        validated_data['date'] = lead.date
        validated_data['vehicle_runs'] = lead.vehicle_runs
        validated_data['ship_via_id'] = lead.ship_via_id
        validated_data['email'] = lead.email
        validated_data['price'] = float(lead.price)

        if validated_data['tarif'] == '1':
            validated_data['final_price'] = float(lead.price_first_tarif)
        elif validated_data['tarif'] == '2':
            validated_data['final_price'] = float(lead.price_second_tarif)
    
        return super().create(validated_data)

    def to_representation(self, instance):
        serializers = AplicationViewSerializer(instance, context={'request': self.context.get('request')})
        return serializers.data


# reviews serializer
class ReviewSerializer(serializers.ModelSerializer):
    title = JsonFieldSerializer()
    text = JsonFieldSerializer()
    image = ThumbnailSerializer(alias='avatar')

    class Meta:
        model = Reviews
        fields = '__all__'



# short application serializer
class ShortApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortApplication
        fields = '__all__'
