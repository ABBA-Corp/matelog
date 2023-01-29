from rest_framework import serializers
from admins.models import Services, Articles, ArticleImages, StaticInformation, AboutUs, Languages, Translations
from easy_thumbnails.templatetags.thumbnail import thumbnail_url


class ThumbnailSerializer(serializers.ImageField):
    def __init__(self, alias, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alias = alias

    def to_representation(self, instance):
        url = thumbnail_url(instance, self.alias)
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


# articles
class ArticleSerializer(serializers.ModelSerializer):
    title = JsonFieldSerializer()
    subtitle = JsonFieldSerializer()
    body = JsonFieldSerializer()
    created_date = serializers.DateField(format="%Y.%m.%d")
    image = ThumbnailSerializer(alias='prod_photo')
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Articles
        fields = '__all__'



# service serializer
class ServiceSerializer(serializers.ModelSerializer):
    title = JsonFieldSerializer()
    sub_title = JsonFieldSerializer()
    deckription = JsonFieldSerializer()
    image = ThumbnailSerializer(alias='prod_photo')


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

