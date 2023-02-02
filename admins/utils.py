import string
from .models import Articles, Languages, Translations, TranlsationGroups, StaticInformation, AdminInputs
import datetime
from django.db.models import Q
import json
from django.apps import apps
from django.core.paginator import Paginator
from django.http import JsonResponse, QueryDict
import re
from django.core.files.storage import default_storage

# get request.data in JSON
def serialize_request(model, request):
    langs = Languages.objects.filter(active=True)

    data_dict = {}

    for field in model._meta.fields:
        field_dict = {}
        if str(field.get_internal_type()) == 'JSONField':
            for key in request.POST:
                key_split = str(key).split('#')
                if key_split[0] == str(field.name):
                    for lang in langs:
                        if key_split[-1] == lang.code:
                            field_dict[lang.code] = request.POST.get(key)
            data_dict[str(field.name)] = field_dict
        else:
            value = request.POST.get(str(field.name))
            if value and field.get_internal_type() != 'BooleanField':
                data_dict[str(field.name)] = value
            elif field.get_internal_type() == 'BooleanField':
                    data_dict[str(field.name)] = True
            
    return data_dict


# search_paginate
def search_pagination(request):
    url = request.path + '?'

    if 'q=' in request.get_full_path():
        if '&' in request.get_full_path():
            url = request.get_full_path().split('&')[0] + '&'
        else:
            url = request.get_full_path() + '&'

    return url


# get model fields
def get_model_fields(model):
    json_fields = {}
    try:
        json_fields = AdminInputs.objects.get(id=1)
    except:
        json_fields = AdminInputs().save()

    model_name = model._meta.verbose_name.title()
    try:
        data_lst = json_fields.inputs.get(model_name)
    except:
        data_lst = []

    return data_lst


# list to queryset
def list_to_queryset(model_list):
    if len(model_list) > 0:
        return model_list[0].__class__.objects.filter(
            pk__in=[obj.pk for obj in model_list])
    else:
        return []


# list of dicts to queryset
def list_of_dicts_to_queryset(list, model):
    if len(list) > 0:
        return model.objects.filter(id__in=[int(obj['id']) for obj in list])
    else:
        return []



# search translations
def search_translation(query, queryset):
    langs = Languages.objects.all()
    endlist = []
    if query and query != '':
        for item in queryset:
            for lang in langs:
                if query.lower() in str(item.value[lang.code]).lower() or query.lower() in str(item.key).lower():
                    endlist.append(item)
                continue
    
        queryset = list_to_queryset(endlist)
    
    return queryset



# pagination
def paginate(queryset, request, number):
    paginator = Paginator(queryset, number)

    try:
        page_obj = paginator.get_page(request.GET.get("page"))
    except:
        page_obj = paginator.get_page(request.GET.get(1))

    return page_obj


# get lst data
def get_lst_data(queryset, request, number):
    lst_one = paginate(queryset, request, number)
    lst_two = range(1, len(queryset) + 1)

    return dict(pairs=zip(lst_one, lst_two))




# search
def search(query, queryset, fields: list, model):
    langs = Languages.objects.all()
    endlist = list()

    if query is None:
        return queryset

    queryset = queryset.values()
    
    for field in fields:
        for item in queryset:
            for lang in langs:
                if query.lower() in str(item[field][lang.code]).lower():
                    if item['id'] not in [it['id'] for it in endlist]:
                        endlist.append(item)
                continue

    queryset = list_of_dicts_to_queryset(endlist, model)

    return queryset


# langs save
def lang_save(form, request):
    lang = form.save()
    key = request.POST.get('dropzone-key')
    sess_image = request.session.get(key)

    if sess_image:
        lang.icon = sess_image[0]['name']
        request.session[key].remove(sess_image[0])
        request.session.modified = True
        lang.save()

    if lang.default:
        for lng in Languages.objects.exclude(id=lang.id):
            lng.default = False
            lng.save()

    return lang




# is valid
def is_valid_field(data, field):
    lang = Languages.objects.filter(default=True).first()
    try:
        val = data.get(field, {}).get(lang.code, '')
    except:
        return False

    print(val == '')
    print('!!!!', val != '')

    return val != ''



# clean text
def clean_text(str):
    for char in string.punctuation:
        str = str.replace(char, ' ')

    return str.replace(' ', '')