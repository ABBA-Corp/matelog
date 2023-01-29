from .models import Translations
from rest_framework import serializers


class TranslationSerializer(serializers.ModelSerializer):
    group = serializers.ReadOnlyField(source='group.sub_text')

    class Meta:
        model = Translations
        fields = '__all__'

