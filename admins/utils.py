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
        if field.name == 'id':
            continue

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
                if field.name in request.POST:
                    data_dict[str(field.name)] = True
                elif field.name not in request.POST:
                    data_dict[str(field.name)] = False
            
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
        query = query.lower()
        for item in queryset:
            for lang in langs:
                if query in str(item.value.get(lang.code, '')).lower() or query in str(item.key).lower() or query in str(item.group.sub_text + '.' + item.key).lower():
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
    page = request.GET.get('page')

    if page is None or int(page) == 1:
        lst_two = range(1, number + 1)
    else:
        start = (int(page) - 1) * number + 1
        end = int(page) * number

        if end > len(queryset):
            end = len(queryset)

        lst_two = range(start, end + 1)


    return dict(pairs=zip(lst_one, lst_two))




# search
def search(request, queryset, fields: list):
    query = request.GET.get("q", '')

    if query == '':
        return queryset 

    langs = Languages.objects.filter(active=True)
    query_str = ''
    for lang in langs:
        query_str += f'"$.{lang.code}",'

    if langs.exists():
        end_set = set()
        for field in fields:
            qs = queryset.extra(where=[f'LOWER({field} ::varchar) LIKE %s'], params=[f'%{query.lower()}%'])

            for item in qs:
                end_set.add(item)

        queryset = list_to_queryset(list(end_set))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

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



# requeired field errors
def required_field_validate(fields: list, data):
    error = {}

    for field in fields:
        if field not in data:
            error[field] = 'This field is reuqired'

    return error
