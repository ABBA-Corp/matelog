from django.template.defaulttags import register
from django.core.files.storage import default_storage
import os
from django.conf import settings
import json
from easy_thumbnails.templatetags.thumbnail import thumbnail_url, get_thumbnailer

@register.simple_tag
def image_thumb(image, **kwargs):
    alias_key = kwargs.get('alias')
    request = kwargs.get('request')

    alias = settings.THUMBNAIL_ALIASES.get('').get(alias_key)
    if alias is None:
        return None

    size = alias.get('size')[0]
    url = None

    if image:
        orig_url = image.path.split('.')
        thb_url = '.'.join(orig_url) + f'.{size}x{size}_q85.{orig_url[-1]}'
        if default_storage.exists(thb_url):
            print("if")
            last_url = image.url.split('.')
            url = '.'.join(last_url) + f'.{size}x{size}_q85.{last_url[-1]}'
        else:
            print('else')
            url = get_thumbnailer(image)[alias_key].url

    if url == '' or url is None:
        return None

    if request is not None:
        return request.build_absolute_uri(url)

    return url
