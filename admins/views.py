from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from .models import Articles, Languages, Translations, TranlsationGroups, StaticInformation, AdminInputs, ArticleCategories, FAQ, ArticleImages
from .models import Events, EventImages, ImageGalery, VideoGalery, AboutUs, Services, MetaTags, telephone_validator
from .forms import LngForm, UserForm
from django.core.exceptions import ValidationError
import datetime
from django.db.models import Q
import json
from django.apps import apps
from django.http import JsonResponse, QueryDict, HttpResponseRedirect
from django.core.files.storage import default_storage
from .utils import *
from django.core.paginator import Paginator
from .serializers import TranslationSerializer
from rest_framework.response import Response
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from main.models import CarsModel, CarMarks, States, City, Leads
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import logout
import os
# Create your views here.

# home admin
def home(request):
    return render(request, 'admin/base_template.html')


# delete model item
def delete_item(request):
    model_name = request.POST.get("model_name_del")
    app_name = request.POST.get('app_name_del')
    id = request.POST.get('item_id')
    url = request.POST.get("url")

    try:
        model = apps.get_model(model_name=model_name, app_label=app_name)
        model.objects.get(id=int(id)).delete()
    except:
        pass

    return redirect(url)



def delete_alot(request):
    model_name = request.POST.get("model_name")
    app_name = request.POST.get('app_name')
    id_list = request.POST.getlist('id')

    print(id_list)
    print(app_name, model_name)
    url = request.POST.get('url')

    #try:
    model = apps.get_model(model_name=model_name, app_label=app_name)
    for item in id_list:
        print(item)
        if f'id[{item}]' in request.POST:
            print('yes')
            model.objects.get(id=int(item)).delete()
    #except:
    #    pass


    return redirect(url)



# save images
def save_images(request):
    print(request.FILES)
    if request.method == 'POST':
        key = request.POST.get("key")
        file = request.FILES.get('file')
        id  = request.POST.get("id")

        request.session[key] = request.session.get(key, [])
        file_name = default_storage.save('dropzone/' + file.name, file)

        data = {
            'id': id,
            'name': file_name
        }
        
        request.session[key].append(data)
        request.session.modified = True

    return JsonResponse(file_name, safe=False)



# del lang icon
def del_lang_icon(request):
    id = request.POST.get("item_id")
    url = request.POST.get('url')
    try:
        Languages.objects.get(id=int(id)).icon.delete(save=False)
    except:
        pass


    return redirect(url)


# delete article group image
def delete_article_group_img(request):
    id = request.POST.get('item_id')

    try:
        ArticleCategories.objects.get(id=int(id)).image.delete(save=False)
    except:
        return JsonResponse("error", safe=False)

    return JsonResponse('success', safe=False)


# add static image
def add_static_image(request):
    url = request.POST.get('url')
    key = request.POST.get("key")
    file = request.FILES.get('file')

    print(file)

    try:
        model = StaticInformation.objects.get(id=1)

        if key == 'logo1':
            model.logo_first = file
        elif key == 'logo2':
            model.logo_second = file

        model.save()
    except:
        pass

    return redirect(url)


# delete article images
def del_statics_image(request):
    url = request.POST.get('url')
    key = request.POST.get("key")

    try:
        model = StaticInformation.objects.get(id=1)

        if key == 'logo1':
            model.logo_first.delete()
        elif key == 'logo2':
            model.logo_second.delete()
    except:
        pass

    return redirect(url)


# delete image
def delete_image(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        file = request.POST.get("file")
        
        if request.session.get(key):
            for it in request.session[key]:
                if it['name'] == file:
                    request.session[key].remove(it)
                    request.session.modified = True
        

    return redirect(request.META.get("HTTP_REFERER"))



# articles create
class ArticleCreateView(CreateView):
    model = Articles
    template_name = 'admin/new_article.html'
    fields = "__all__"
    success_url = 'articles_list'

    def get_context_data(self, **kwargs):
        context = super(ArticleCreateView, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')
        context['lang'] = Languages.objects.filter(default=True).first()
        context['fields'] = get_model_fields(self.model)
        context['categories'] = ArticleCategories.objects.all()
        context['dropzone_key'] = self.model._meta.verbose_name
        context['images'] = []

        
        if self.request.session.get(context['dropzone_key']):
            context['images'] = list({'name': it['name'], 'id': clean_text(it['name'])} for it in self.request.session[context['dropzone_key']] if it['id'] == '')

        return context

    def form_valid(self, form):
        return None


    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        data_dict['created_date'] = data_dict.get('created_date', str(datetime.date.today()))
        data_dict['author'] = request.user
        key = request.POST.get('dropzone-key')
        categories = request.POST.getlist('categories[]')
        
        data = self.get_context_data()

        if is_valid_field(data_dict, 'title') == False:
            data['request_post'] = data_dict
            data['error'] = 'This field is required.'
            return render(request, self.template_name, data)

        try:
            article = Articles(**data_dict)
            article.full_clean()
            article.save()
            if categories:
                ctg_queryset = [ArticleCategories.objects.get(id=int(it)) for it in categories]
                article.category.set(ctg_queryset)

            key = self.model._meta.verbose_name
            sess_images = request.session.get(key)

            if sess_images and len([it for it in request.session.get(key) if it['id'] == '']) > 0:
                image = [it for it in request.session.get(key) if it['id'] == ''][0]
            
                article.image = image['name']
                article.save()
                request.session.get(key).remove(image)
                request.session.modified = True

            meta_dict = serialize_request(MetaTags, request)
            try:
                print(meta_dict)
                meta = MetaTags(**meta_dict)
                meta.full_clean()
                meta.save()
                article.meta = meta
                article.save()
            except:
                pass

        except ValidationError:
            print(ValidationError)

        return  redirect('articles_list')#redirect("")


# articles list
class ArticlesList(ListView):
    model = Articles
    template_name = 'admin/articles_list.html'

    def get_queryset(self):
        queryset = Articles.objects.all()
        queryset = search(self.request, queryset, ['title', 'body'], self.model)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ArticlesList, self).get_context_data(**kwargs)

        context['q'] = self.request.GET.get('q')
        context['lang'] = Languages.objects.filter(active=True).filter(default=True).first()
        context['objects'] = get_lst_data(self.get_queryset(), self.request, 20)
        context['page_obj'] = paginate(self.get_queryset(), self.request, 20)
        context['url'] = search_pagination(self.request)

        return context


# delete article
def del_article(request):
    id = request.POST.get('id')
    url = request.POST.get("url")

    try:
        Articles.objects.get(id=int(id)).delete()
    except:
        pass

    return redirect(url)

# article update
class ArticleUpdate(UpdateView):
    model = Articles
    fields = '__all__'
    template_name = 'admin/new_article.html'
    success_url = 'articles_list'
    
    def get(self, request, *args, **kwargs):
        if request.user != self.get_object().author:
            return redirect('articles_list')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdate, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(active=True).order_by("-default")
        context['lang'] = Languages.objects.filter(active=True).filter(default=True).first()
        context['fields'] = get_model_fields(self.model)
        context['categories'] = ArticleCategories.objects.all()
        context['dropzone_key'] = self.model._meta.verbose_name

        return context

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        url = request.POST.get("url")
        key = self.model._meta.verbose_name

        data = self.get_context_data()
        if is_valid_field(data_dict, 'title') == False:
            data['request_post'] = data_dict
            data['error'] = 'This field is required.'
            return render(request, self.template_name, data)


        try:
            file = [it for it in request.session.get(key, []) if it['id'] == str(self.get_object().id)][0]
        except:
            file = None
        categories = request.POST.getlist('categories[]')

        
        try:
            instance = self.get_object()

            for attr, value in data_dict.items(): 
                setattr(instance, attr, value)
            
            instance.save()

            if categories:
                ctg_queryset = [ArticleCategories.objects.get(id=int(it)) for it in categories]
                instance.category.set(ctg_queryset)

            if file:
                instance.image = file['name']
                for it in request.session.get(key): 
                    if it['id'] == str(self.get_object().id):
                        try:
                            request.session.get(key).remove(it)
                            request.session.modified = True
                        except:
                            pass
                instance.save()

            meta_dict = serialize_request(MetaTags, request)
            try:
                for attr, value in meta_dict.items():
                    if str(attr) != 'id':
                        setattr(instance.meta, attr, value)
                instance.meta.save()
            except:
                pass

        except ValidationError:
            print(ValidationError)

            return reverse_lazy('articles_edit')

        return redirect(url)


# langs list
class LangsList(ListView):
    model = Languages
    context_object_name = 'langs'
    template_name = 'admin/lang_list.html'

    def get_queryset(self):
        queryset = Languages.objects.all().order_by('-default')
        query = self.request.GET.get("q")
        if query == '':
            query = None

        if query:
            queryset = queryset.filter(Q(name__iregex=query) | Q(code__iregex=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(LangsList, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get("q")
        context['langs'] = get_lst_data(self.get_queryset(), self.request, 20)
        context['page_obj'] = paginate(self.get_queryset(), self.request, 20)
        context['url'] = search_pagination(self.request)

        return context


# langs create
class LngCreateView(CreateView):
    model = Languages
    form_class = LngForm
    success_url = '/admin/langs'
    template_name = "admin/lng_create.html"

        
    def form_valid(self, form):
        lang_save(form, self.request)


        return redirect('langs_list')
        
    def get_context_data(self, **kwargs):
        context = super(LngCreateView, self).get_context_data(**kwargs) 
        context['fields'] = get_model_fields(self.model)
        context['dropzone_key'] = self.model._meta.verbose_name
        context['images'] = []

        if self.request.session.get(context['dropzone_key']):
            context['images'] = list({'name': it['name'], 'id': str(it['name']).replace('/', '').replace('.', '')} for it in self.request.session[context['dropzone_key']] if it['id'] == '')

        return context


# langs update
class LangsUpdate(UpdateView):
    model = Languages
    form_class = LngForm
    success_url = '/admin/langs'
    template_name = "admin/lng_create.html"


    def get_context_data(self, **kwargs):
        context = super(LangsUpdate, self).get_context_data(**kwargs)
        context['fields'] = get_model_fields(self.model)
        context['dropzone_key'] = self.model._meta.verbose_name

        return context


    def form_valid(self, form):
        lang_save(form, self.request)


        return redirect('langs_list')


# langs delete
def delete_langs(request):
    if request.method == 'POST':
        lng_id = request.POST.get("id")
        try:
            Languages.objects.get(id=int(lng_id)).delete()
        except:
            pass

        url = request.POST.get("url", request.META.get('HTTP_REFERER'))

        return redirect(url)



# static update
class StaticUpdate(UpdateView):
    model = StaticInformation
    fields = "__all__"
    template_name = 'admin/static_add.html'
    success_url = '/admin/'

    def get_object(self):
        try:
            object = StaticInformation.objects.first()
        except:
            object = StaticInformation.objects.create()

        return object


    def get_context_data(self, **kwargs):
        context = super(StaticUpdate, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')
        context['dropzone_key'] = self.model._meta.verbose_name


        return context

    def form_valid(self, form):
        return None

    
    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(StaticInformation, request)
        instance = self.get_object()

        data = self.get_context_data()
        if is_valid_field(data_dict, 'title') == False:
            data['request_post'] = data_dict
            data['error'] = 'This field is required'
            return render(request, self.template_name, data)
        else:
            for attr, value in data_dict.items():
                setattr(instance, attr, value)
            instance.save()

        return redirect('static_info')


def class_list():
    my_apps = ['admins']
    my_app_models = [apps.all_models[name] for name in my_apps]
    return my_app_models

# form setting
class FormSettings(UpdateView):
    model = AdminInputs
    template_name = 'admin/form_settings.html'
    fields = "__all__"


    def get_object(self):
        try:
            object = AdminInputs.objects.get(id=1)
        except:
            object = AdminInputs().save()

        return object


    def get_context_data(self, **kwargs):
        context = super(FormSettings, self).get_context_data(**kwargs)
        models = class_list()

        context['models'] = []

        for model in models:
            for key in model:
                if model[key]._meta.verbose_name.title() != 'Admin Inputs':
                    data = {}
                    data['title']= model[key].__name__
                    data['name'] = model[key]._meta.verbose_name.title()
                    data['fields'] = []

                    for field in model[key]._meta.get_fields():
                        if field.name != 'id':
                            data['fields'].append(field.name)

                    context['models'].append(data)

        settings_fields = {}
        try:
            for key in self.get_object().inputs:
                data_list = []
                for item in self.get_object().inputs[key]:
                    data_list.append(item['field'])
                
                settings_fields[key] = data_list
        except:
            pass
        
        context['set_fields'] = settings_fields
        print(context['set_fields'])

        return context


    def post(self, request, *args, **kwargs):
        request_data = []
        settings = self.get_object()

        for key in request.POST:
            try:
                data = {}
                data['key'] = json.loads(str(key))
                data['value'] = request.POST[key]
                request_data.append(data)
            except:
                pass
        
        boolens = []
        for data in request_data:
            if data['key']['type'] == 'bool':
                data_tuple = (data['key']['model'], data['key']['field'])
                boolens.append(data_tuple)


        final_data = {}
        for data in request_data:
            model_name = data['key']['model']
            field = data['key']['field']

            if (model_name, field) in boolens and data['key']['type'] == 'label':

                final_data[model_name] = final_data.get(model_name, [])

                data_dict = {
                    'field': data['key']['field'],
                    'label': data['value']
                }
                final_data[model_name].append(data_dict)
            
        print(final_data)
        settings.inputs = final_data
        settings.save()

        return redirect(request.META.get("HTTP_REFERER"))



# translations list
class TranslationList(ListView):
    model = Translations
    template_name = 'admin/translation_list.html'
    
    def get_queryset(self):
        queryset = Translations.objects.all()
        query = self.request.GET.get("q")
        queryset = search_translation(query, queryset)

        return queryset

    
    def get_context_data(self, **kwargs):
        context = super(TranslationList, self).get_context_data(**kwargs)
        context['groups'] = TranlsationGroups.objects.all()
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')
        context['url'] = search_pagination(self.request)

        # pagination
        page_obj = paginate(self.get_queryset(), self.request, 20)
        context['page_obj'] = page_obj

        lst_one = page_obj
        lst_two = range(1, len(self.get_queryset()) + 1)

        context['translations'] = dict(pairs=zip(lst_one, lst_two))

        return context



# translation group
class TranslationGroupDetail(DetailView):
    model = TranlsationGroups
    template_name = 'admin/translation_list.html'

    def get_context_data(self, **kwargs):
        context = super(TranslationGroupDetail, self).get_context_data(**kwargs)
        context['groups'] = TranlsationGroups.objects.all()
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')
        lst_one = self.get_object().translations.order_by('-id')

        # search
        query = self.request.GET.get("q")
        lst_one = search_translation(query, lst_one)

        
        # range
        lst_two = range(1, len(lst_one) + 1)

        # zip 2 lst
        context['translations'] = dict(pairs=zip(lst_one, lst_two))

        return context



# transtion update
def translation_update(request):
    if request.method == 'GET':
        id = request.GET.get('id')

        try:
            translation = Translations.objects.get(id=int(id))
            serializer = TranslationSerializer(translation)

            return JsonResponse(serializer.data)
        except:
            return JsonResponse({'error': 'error'}, safe=False)

    elif request.method == 'POST':
        data = serialize_request(Translations, request)
        id = request.POST.get("id")
        lang = Languages.objects.filter(active=True).filter(default=True).first()

        if data.get('value').get(lang.code, '') == '':
            return JsonResponse({'lng_error': 'This language is required'})
        
        try:
            translation = Translations.objects.get(id=int(id))
            key = data.get('key', '')

            if key == '':
                return JsonResponse({'key_error': 'Key is required'})
            
            if str(key) in [str(it.key) for it in Translations.objects.exclude(id=translation.id)]:
                return JsonResponse({'key_error': 'Key is already in use'})
            
            translation.key = key
            translation.value = data['value']
            translation.full_clean()
            translation.save()
        except:
            return JsonResponse('some error', safe=False)

        serializer = TranslationSerializer(translation)

        return JsonResponse(serializer.data)



# translations delete
def delete_translation(request):
    id = request.POST.get("id")
    url = request.POST.get("url")
    try:
        Translations.objects.get(id=int(id)).delete()
    except:
        return JsonResponse({'error': 'Id is invalid'})

    return redirect(url)


# add translation group
def add_trans_group(request):
    if request.method == 'POST':
        data_dict = serialize_request(TranlsationGroups, request)

        print(TranlsationGroups.objects.values_list('sub_text'))

        if data_dict.get('sub_text', '') == '':
            return JsonResponse({'key_error': 'Sub text is required'})
        elif (data_dict.get('sub_text'), ) in TranlsationGroups.objects.values_list('sub_text'):
            return JsonResponse({'key_error': 'This key is already in use'})
        

        try:
            transl_group = TranlsationGroups(**data_dict)
            transl_group.full_clean()
            transl_group.save()
        except ValidationError:
            return JsonResponse({'title_error': 'This title is empty or already in use'})

        data = {
            'id': transl_group.id,
            'name': transl_group.title,
            'key': transl_group.sub_text
        }
        return JsonResponse(data)



# translation group udate
class TranslationGroupUdpate(UpdateView):
    model = TranlsationGroups
    template_name = 'admin/translation_edit.html'
    fields = '__all__'
    success_url = '/admin/translations'

    def get_context_data(self, **kwargs):
        context = super(TranslationGroupUdpate, self).get_context_data(**kwargs)
        context['groups'] = TranlsationGroups.objects.all()
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')
        context['lng'] = Languages.objects.filter(active=True).filter(default=True).first()
        lst_one = self.get_object().translations.all()


        # range
        lst_two = range(1, len(lst_one) + 1)

        # zip 2 lst
        context['translations'] = dict(pairs=zip(lst_one, lst_two))

        return context

    
    def post(self, request, *args, **kwargs):
        transls = list(self.get_object().translations.all())
        langs = Languages.objects.filter(active=True).order_by('-default')
        lang = Languages.objects.filter(active=True).filter(default=True).first()
        items_count = request.POST.get("item_count")


        data = []
        for l in range(1, int(items_count) + 1):
            new_data = {}
            new_data['id'] = l
            new_data['key'] = request.POST[f'key[{l}]']
            new_data['values'] = []
            for lng in langs:
                new_data['values'].append({'key': f'value[{l}][{lng.code}]', 'value': request.POST[f'value[{l}][{lng.code}]'], 'def_lang': lang.code, 'lng': lng.code})
            
            data.append(new_data)


        print(data)

        objects = dict(pairs=zip(data, list(range(1, int(items_count) + 1))))



        for i in range(len(transls)):
            transls[i].key = request.POST.get(f'key[{i + 1}]', '')
            
            if transls[i].key == '':
                return render(request, template_name=self.template_name, context={'key_errors': {str(i+1): 'Key is required'},  'new_objects': objects, 'langs': langs, 'len': int(items_count) + 1})

            in_default_lng = request.POST.get(f'value[{i+1}][{lang.code}]', '')

            if in_default_lng == '':
                return render(request, template_name=self.template_name, context={'lng_errors': {str(i+1): 'This language is required'}, 'new_objects': objects, 'langs': langs, 'len': int(items_count) + 1})

            value_dict = {}
            for lang in langs:
                value_dict[str(lang.code)] = request.POST[f'value[{i + 1}][{lang.code}]']

            transls[i].value = value_dict
            try:
                transls[i].full_clean()
                transls[i].save()
            except:
                return render(request, template_name=self.template_name, context={'key_errors': {str(i): 'Key is alredy in use'},  'new_objects': objects, 'langs': langs, 'len': items_count})

                
        for i in range(len(transls) + 1, int(items_count) + 1):
            new_trans = Translations()
            data = {}
            new_trans.key = request.POST.get(f'key[{i}]', '')

            if new_trans.key == '':
                return render(request, template_name=self.template_name, context={'key_errors': {str(i): 'Key is required'},  'new_objects': objects, 'langs': langs, 'len': items_count})


            value_dict = {}
            in_default_lng = request.POST.get(f'value[{i}][{lang.code}]', '')

            
            if in_default_lng == '':
                return render(request, template_name=self.template_name, context={'lng_errors': {str(i): 'This language is required'}, 'new_objects': objects, 'langs': langs, 'len': items_count})


            for lang in langs:
                value_dict[str(lang.code)] = request.POST[f'value[{i}][{lang.code}]']
        
            new_trans.value = value_dict
            new_trans.group = self.get_object()
            
            try:
                new_trans.full_clean()
                new_trans.save()
            except:
                return render(request, template_name=self.template_name, context={'key_errors': {str(i): 'Key is alredy in use'}, 'new_objects': objects, 'langs': langs, 'len': items_count})


        return redirect('transl_group_detail', pk=self.get_object().id)


# article ctg list
class ArticleCtgList(ListView):
    model = ArticleCategories
    template_name = 'admin/article_ctg.lst.html'
    
    def get_queryset(self):
        queryset = super(ArticleCtgList, self).get_queryset()
        return search(self.request, queryset, ['name'], self.model)

    def get_context_data(self, **kwargs):
        context = super(ArticleCtgList, self).get_context_data(**kwargs)
        context['objects'] = get_lst_data(self.get_queryset(), self.request, 20)
        context['lang'] = Languages.objects.filter(active=True).filter(default=True).first()
        context['page_obj'] = paginate(self.get_queryset(), self.request, 20)
        context['url'] = search_pagination(self.request)

        return context



# add article ctg
class AddArticleCtg(CreateView):
    model = ArticleCategories
    template_name = 'admin/article_ctg_form.html'
    fields = '__all__'
    success_url = 'article_ctg_list'


    def get_context_data(self, **kwargs):
        context = super(AddArticleCtg, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')
        context['categories'] = ArticleCategories.objects.all()
        context['fields'] = get_model_fields(self.model)
        context['lang'] = Languages.objects.filter(active=True).filter(default=True).first()
        context['dropzone_key'] = self.model._meta.verbose_name
        context['images'] = []

        if self.request.session.get(context['dropzone_key']):
            context['images'] = list({'name': it['name'], 'id': clean_text(it['name'])} for it in self.request.session[context['dropzone_key']] if it['id'] == '')

        return context


    def form_valid(self, form):
        return None


    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        parent = request.POST.get('parent')


        data = self.get_context_data()
        try:
            data_dict['parent'] = ArticleCategories.objects.get(id=int(data_dict.get('parent')))
        except:
            if data_dict.get("parent"):
                del data_dict['parent']

        if is_valid_field(data_dict, 'name') == False:
            data['request_post'] = data_dict
            data['error'] = 'This field is required.'
            return render(request, self.template_name, data)
        else:
            try:
                art_ctg = ArticleCategories(**data_dict)
                art_ctg.full_clean()
                art_ctg.save()

                key = self.model._meta.verbose_name
                sess_images = request.session.get(key)

                if sess_images and len([it for it in request.session.get(key) if it['id'] == '']) > 0:
                    image = [it for it in request.session.get(key) if it['id'] == ''][0]
                
                    art_ctg.image = image['name']
                    art_ctg.save()
                    request.session.get(key).remove(image)
                    request.session.modified = True
            except:
                pass
        


        return redirect('article_ctg_list')


# article ctg edit
class ArticleCtgEdit(UpdateView):
    model = ArticleCategories
    fields = "__all__"
    template_name = 'admin/article_ctg_form.html'
    success_url = '/admin/article_categories'

    def get_context_data(self, **kwargs):
        context = super(ArticleCtgEdit, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')
        context['categories'] = ArticleCategories.objects.exclude(id=self.get_object().id)
        context['fields'] = get_model_fields(self.model)
        context['lang'] = Languages.objects.filter(active=True).filter(default=True).first()
        context['dropzone_key'] = self.model._meta.verbose_name

        return context


    def form_valid(self, form):
        return None


    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, self.request)
        key = self.model._meta.verbose_name
        try:
            file = [it for it in request.session.get(key, []) if it['id'] == str(self.get_object().id)][0]
        except:
            file = None

        try:
            data_dict['parent'] = ArticleCategories.objects.get(id=int(data_dict.get('parent')))
        except:
            if data_dict.get("parent"):
                del data_dict['parent']

        data = self.get_context_data()
        if is_valid_field(data_dict, 'name') == False:
            data['request_post'] = data_dict
            data['error'] = 'This field is required.'
            return render(request, self.template_name, data)


        instance = self.get_object()

        for attr, value in data_dict.items():
            setattr(instance, attr, value)

        instance.save()

        if file:
            instance.image = file['name']
            for it in request.session.get(key): 
                if it['id'] == str(self.get_object().id):
                    try:
                        request.session.get(key).remove(it)
                        request.session.modified = True
                    except:
                        pass
            instance.save()
        
        return redirect('article_ctg_list')


# article category delete
def article_ctg_del(request):
    try:
        ArticleCategories.objects.get(id=request.POST.get("id")).delete()
    except:
        pass

    return redirect(request.POST.get("url"))


# faq list
class FAQlist(ListView):
    model = FAQ
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(FAQlist, self).get_context_data(**kwargs)
        context['lang'] = Languages.objects.filter(active=True).filter(default=True)
        queryset = self.get_queryset()
        queryset = search(self.request, queryset, ['answer', 'question'])

    
        context['objects'] = get_lst_data(queryset, self.request, 20)
        context['page_obj'] = paginate(self.get_queryset(), self.request, 20)
        context['url'] = search_pagination(self.request)

        return context



# faq create
class FAQcreate(CreateView):
    model = FAQ
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(FAQcreate, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')

        return context

    
    def post(self, request, *args, **kwargs):
        data_dict = serialize_request(self.model, request)
        faq = FAQ(**data_dict)
        faq.save()


        return redirect('/')


# faq update
class FAQupdate(UpdateView):
    model = FAQ
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(FAQupdate, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')

        return context


    def post(self, request, *args, **kwargs):
        data_dict = serialize_request(self.model, request)
        instance = self.get_object()

        for attr, value in data_dict.items():
            setattr(instance, attr, value)
        instance.save()

        return redirect(request.META.get("HTTP_REFERER"))




# event list
class EventsList(ListView):
    model = Events
    paginate_by = 10


    def get_queryset(self):
        queryset = super(EventsList, self).get_queryset()
        return search(self.request, queryset, ['title'], self.model)

    def get_context_data(self, **kwargs):
        context = super(EventsList, self).get_context_data(**kwargs)
        context['lang'] = Languages.objects.filter(active=True).filter(default=True).first()
        context['page_obj'] = paginate(self.get_queryset(), self.request, 20)
        context['url'] = search_pagination(self.request)
        context['objects'] = get_lst_data(self.get_queryset(), self.request, 20)

        return context


# events create
class EventsCreate(CreateView):
    model = Events
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(EventsCreate, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.all().order_by('-default')

        return context

    def form_valid(self, form):
        return None

    def post(self, request, *args, **kwargs):
        data_dict = serialize_request(self.model, request)
        event = Events(**data_dict)
        event.save()

        return redirect('/')



# events update
class EventsUpdate(UpdateView):
    model = Events
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super(EventsUpdate, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')

        return context

    def form_valid(self, form):
        return None


    def post(self, request, *args, **kwargs):
        data_dict = serialize_request(self.model, request)
        instance = self.get_object()

        for attr, value in data_dict.items():
            setattr(instance, attr, value)
        instance.save()


        return redirect(request.META.get("HTTP_REFERER"))
        


# about us
class AboutUsView(UpdateView):
    model = AboutUs
    fields = "__all__"
    template_name = 'admin/about_us.html'
    success_url = '/admin/about_us'

    def form_valid(self, form):
        return None

    def get_object(self):
        try:
            model = AboutUs.objects.get(id=1)
        except:
            model = AboutUs.objects.create()

        return model


    def get_context_data(self, **kwargs):
        context = super(AboutUsView, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')

        return context


    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        instance = self.get_object()
        url = request.POST.get("url")

        data = self.get_context_data()
        if is_valid_field(data_dict, 'title_one') == False:
            data['error'] = 'This field is required.'
            data['request_post'] = data_dict
            return render(request, self.template_name, data)


        for attr, value in data_dict.items():
            setattr(instance, attr, value)
        instance.save()

        return redirect('about_us')



# delete about us video
def delete_about_video(request):
    try:
        model = AboutUs.objects.get(id=1)
        model.video.delete(save=False)
    except:
        return JsonResponse("error", safe=False)

    return JsonResponse("success", safe=False)


# set about video
def set_about_video(request):
    video = request.FILES.get("file")
    try:
        model = AboutUs.objects.get(id=1)
    except:
        model = AboutUs().save()
    
    model.video = video
    model.save()

    return JsonResponse('success', safe=False)


    
# services list
class ServicesList(ListView):
    model = Services
    template_name = 'admin/services.html'

    def get_queryset(self):
        queryset = Services.objects.all()
        queryset = search(self.request, queryset, ['title', 'deckription', 'sub_title'], self.model)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ServicesList, self).get_context_data(**kwargs)

        context['q'] = self.request.GET.get('q')
        context['lang'] = Languages.objects.filter(default=True).first()
        context['objects'] = get_lst_data(self.get_queryset(), self.request, 20)
        context['page_obj'] = paginate(self.get_queryset(), self.request, 20)
        context['url'] = search_pagination(self.request)

        return context

    

# services update
class ServicesUpdate(UpdateView):
    model = Services
    fields = '__all__'
    success_url = '/admin/services'
    template_name = 'admin/services_form.html'

    def get_context_data(self, **kwargs):
        context = super(ServicesUpdate, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')
        context['sevices'] = Services.objects.exclude(id=self.get_object().id).exclude(id__in=[it.id for it in self.get_object().children.all()])
        context['lang'] = Languages.objects.filter(active=True).filter(default=True).first()
        context['dropzone_key'] = self.model._meta.verbose_name

        return context
    
    def form_valid(self, form):
        return None

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        url = request.POST.get("url")
        key = self.model._meta.verbose_name
        parent_id = request.POST.get('parent')

        
        data = self.get_context_data()
        if is_valid_field(data_dict, 'title') == False:
            data['request_post'] = data_dict
            data['error'] = 'This field is required.'
            return render(request, self.template_name, data)


        try:
            data_dict['parent'] = Services.objects.get(id=int(parent_id))
        except:
            pass

        try:
            file = [it for it in request.session.get(key, []) if it['id'] == str(self.get_object().id)][0]
        except:
            file = None

        instance = self.get_object()

        for attr, value in data_dict.items():
            setattr(instance, attr, value)

        instance.save()

        if file:
            instance.image = file['name']
            for it in request.session.get(key):
                if it['id'] == str(self.get_object().id):
                    try:
                        request.session.get(key).remove(it)
                        request.session.modified = True
                    except:
                        pass
            instance.save()

        meta_dict = serialize_request(MetaTags, request)
        try:
            for attr, value in meta_dict.items():
                if str(attr) != 'id':
                    setattr(instance.meta_field, attr, value)
            instance.meta_field.save()
        except:
            pass

        return redirect(url)



# services create
class ServiceCreate(CreateView):
    model = Services
    fields = "__all__"
    success_url = '/admin/sevices'
    template_name = 'admin/services_form.html'

    def get_context_data(self, **kwargs):
        context = super(ServiceCreate, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')
        context['sevices'] = Services.objects.all()
        context['lang'] = Languages.objects.filter(active=True).filter(default=True).first()
        context['dropzone_key'] = self.model._meta.verbose_name
        context['images'] = []

        if self.request.session.get(context['dropzone_key']):
            context['images'] = list({'name': it['name'], 'id': clean_text(str(it['name']))} for it in self.request.session[context['dropzone_key']] if it['id'] == '')

        return context

    def form_valid(self, form):
        return None

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        key = self.model._meta.verbose_name

        data = self.get_context_data()

        if is_valid_field(data_dict, 'title') == False:
            print("if1")
            data['error'] = 'This field is required.'
            data['request_post'] = data_dict
            return render(request, self.template_name, data)


        parent_id = request.POST.get('parent')
        try:
            data_dict['parent'] = Services.objects.get(id=int(parent_id))
        except:
            pass
        print('else1')
        instance = Services(**data_dict)
        instance.full_clean()
        instance.save()

        sess_images = request.session.get(key)

        if sess_images and len([it for it in sess_images if it['id'] == '']) > 0:
            image = [it for it in sess_images if it['id'] == ''][0]
            instance.image = image['name']
            instance.save()
            request.session.get(key).remove(image)
            request.session.modified = True

        meta_dict = serialize_request(MetaTags, request)
        try:
            meta = MetaTags(**meta_dict)
            meta.full_clean()
            meta.save()
            instance.meta_field = meta
            instance.save()
        except:
            pass


        return redirect('services')  # redirect("")



def del_sev_image(request):
    id = request.POST.get('item_id')

    try:
        Services.objects.get(id=int(id)).image.delete(save=False)
    except:
        JsonResponse({'detail': 'error'})

    return JsonResponse('success', safe=False)




# super users list
class AdminsList(ListView):
    model = User
    template_name = 'admin/moterators_list.html'

    def get_queryset(self):
        queryset = User.objects.filter(is_superuser=True)
        queryset = search(self.request, queryset, ['username', 'first_name', 'last_name'], self.model)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(AdminsList, self).get_context_data(**kwargs)

        context['q'] = self.request.GET.get('q')
        context['lang'] = Languages.objects.filter(active=True).filter(default=True).first()
        context['objects'] = get_lst_data(self.get_queryset(), self.request, 20)
        context['page_obj'] = paginate(self.get_queryset(), self.request, 20)
        context['url'] = search_pagination(self.request)

        return context

    
    

# super user create
class AdminCreate(CreateView):
    model = User
    form_class = UserForm
    success_url = '/'
    template_name = 'admin/moder_form.html'

    def form_valid(self, form):
        new_user = form.save()
        new_user.is_superuser = True
        full_name = self.request.POST.get("name")

        if full_name:
            if len(full_name.split(' ')) == 1:
                new_user.first_name = full_name.split(' ')[0]

            if len(full_name.split(' ')) == 2:
                new_user.last_name = full_name.split(' ')[1]

        new_user.save()

        return redirect('admin_list')


# admin udate
class AdminUpdate(UpdateView):
    model = User
    form_class = UserForm
    success_url = '/'
    template_name = 'admin/moder_form.html'    


    def get_context_data(self, **kwargs):
        context = super(AdminUpdate, self).get_context_data(**kwargs)
        context['full_name'] = None

        if self.get_object().first_name:
            context['full_name'] = self.get_object().first_name
        
        if self.get_object().last_name:
            context['full_name'] += self.get_object().last_name

        return context


    def form_valid(self, form):
        user = form.save()
        user.is_superuser = True
        full_name = self.request.POST.get("name")

        if full_name:
            if len(full_name.split(' ')) == 1:
                user.first_name = full_name.split(' ')[0]

            if len(full_name.split(' ')) == 2:
                user.last_name = full_name.split(' ')[1]

        user.save()

        return redirect('admin_list')


# del article image
def delete_article_image(request):
    id = request.POST.get("item_id")

    try:
        Articles.objects.get(id=int(id)).image.delete(save=False)
    except:
        return JsonResponse({'detail': 'error'})

    return JsonResponse('success', safe=False)


# cars
class CarsModelList(ListView):
    model = CarsModel
    template_name = 'admin/car_model_list.html'

    def get_queryset(self):
        queryset = CarsModel.objects.all()
        queryset = search(self.request, queryset, ['name'], self.model)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CarsModelList, self).get_context_data(**kwargs)

        context['objects'] = get_lst_data(self.get_queryset(), self.request, 20)
        context['page_obj'] = paginate(self.get_queryset(), self.request, 20)
        context['url'] = search_pagination(self.request)
        context['lang'] = Languages.objects.filter(active=True).filter(default=True).first()

        return context

# add car model
class CarModelCreate(CreateView):
    model = CarsModel
    fields = "__all__"
    template_name = 'admin/car_model_form.html'

    def get_context_data(self, **kwargs):
        context = super(CarModelCreate, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')
        context['lang'] = Languages.objects.filter(default=True).first()
        context['marks'] = CarMarks.objects.all()
        context['veh_types'] = ['Car', 'SUV', 'Pickup']

        return context

    def form_valid(self, form):
        return None

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        mark_id = request.POST.get('mark')
        data = self.get_context_data()

        try:
            mark = CarMarks.objects.get(id=int(mark_id))
        except:
            mark = None

        if mark is None:
            data['request_post'] = data_dict
            data['mark_error'] = 'This field is required.'
            return render(request, self.template_name, data)
        
        if is_valid_field(data_dict, 'name') == False:
            data['request_post'] = data_dict
            data['name_error'] = 'This field is required.'
            return render(request, self.template_name, data)

        data_dict['mark'] = mark

        try:
            car_model = CarsModel(**data_dict)
            car_model.full_clean()
            car_model.save()
        except ValidationError:
            print(ValidationError)
            
        return redirect('car_models')


# car model edit
class CarModelEdit(UpdateView):
    model = CarsModel
    fields = "__all__"
    template_name = 'admin/car_model_form.html'

    def get_context_data(self, **kwargs):
        context = super(CarModelEdit, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')
        context['lang'] = Languages.objects.filter(default=True).first()
        context['marks'] = CarMarks.objects.all()
        context['veh_types'] = ['Car', 'SUV', 'Pickup']

        return context

    def form_valid(self, form):
        return None

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, self.request)
        mark_id = request.POST.get('mark')
        data = self.get_context_data()

        try:
            mark = CarMarks.objects.get(id=int(mark_id))
        except:
            mark = None
        
        if mark is None:
            data['request_post'] = data_dict
            data['mark_error'] = 'This field is required.'
            return render(request, self.template_name, data)

        data = self.get_context_data()
        if is_valid_field(data_dict, 'name') == False:
            data['request_post'] = data_dict
            data['name_error'] = 'This field is required.'
            return render(request, self.template_name, data)

        instance = self.get_object()
        data_dict['mark'] = mark

        for attr, value in data_dict.items():
            setattr(instance, attr, value)

        instance.save()

        return redirect('car_models')
    
    

# car mark list
class CarMarkList(ListView):
    model = CarMarks
    template_name = 'admin/car_marks_list.html'

    def get_queryset(self):
        queryset = CarMarks.objects.all()
        queryset = search(self.request, queryset, ['name'], self.model)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(CarMarkList, self).get_context_data(**kwargs)

        context['objects'] = get_lst_data(self.get_queryset(), self.request, 20)
        context['page_obj'] = paginate(self.get_queryset(), self.request, 20)
        context['url'] = search_pagination(self.request)
        context['lang'] = Languages.objects.filter(active=True).filter(default=True).first()

        return context


# car mark create
class CarMarkCreate(CreateView):
    model = CarMarks
    fields = '__all__'
    template_name = 'admin/car_marks_form.html'

    def get_context_data(self, **kwargs):
        context = super(CarMarkCreate, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')
        context['lang'] = Languages.objects.filter(default=True).first()

        return context
    
    def form_valid(self, form):
        return None

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        data = self.get_context_data()

        if is_valid_field(data_dict, 'name') == False:
            data['request_post'] = data_dict
            data['error'] = 'This field is required.'
            return render(request, self.template_name, data)

        try:
            car_mark = CarMarks(**data_dict)
            car_mark.full_clean()
            car_mark.save()
        except:
            pass

        return redirect('car_makes_list')


# car mark edit
class CarMarkEdit(UpdateView):
    model = CarMarks
    fields = '__all__'
    template_name = 'admin/car_marks_form.html'

    def get_context_data(self, **kwargs):
        context = super(CarMarkEdit, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')
        context['lang'] = Languages.objects.filter(default=True).first()

        return context
    
    def form_valid(self, form):
        return None

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, self.request)
        data = self.get_context_data()

        if is_valid_field(data_dict, 'name') == False:
            data['request_post'] = data_dict
            data['error'] = 'This field is required.'
            return render(request, self.template_name, data)

        instance = self.get_object()

        for attr, value in data_dict.items():
            setattr(instance, attr, value)

        instance.save()

        return redirect('car_makes_list')


# states list
class StatesList(ListView):
    model = States
    template_name = 'admin/states.html'

    def get_queryset(self):
        queryset = States.objects.all()
        queryset = search(self.request, queryset, ['name', 'code'], self.model)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(StatesList, self).get_context_data(**kwargs)

        context['objects'] = get_lst_data(self.get_queryset(), self.request, 20)
        context['page_obj'] = paginate(self.get_queryset(), self.request, 20)
        context['lang'] = Languages.objects.filter(active=True).filter(default=True).first()
        context['url'] = search_pagination(self.request)

        return context


# create state
class StatesCreate(CreateView):
    model = States
    fields = '__all__'
    template_name = 'admin/states_form.html'


    def get_context_data(self, **kwargs):
        context = super(StatesCreate, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')
        context['lang'] = Languages.objects.filter(default=True).first()

        return context

    def form_valid(self, form):
        return None

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        data = self.get_context_data()

        code = data_dict.get('code')
        codes = [str(it.code).lower() for it in States.objects.all()]

        if code is None:
            data['request_post'] = data_dict
            data['code_error'] = 'This field is required.'
            return render(request, self.template_name, data)
        elif str(code).lower() in codes:
            data['request_post'] = data_dict
            data['code_error'] = 'This code is already in use.'
            return render(request, self.template_name, data)


        if is_valid_field(data_dict, 'name') == False:
            data['request_post'] = data_dict
            data['name_error'] = 'This field is required.'
            return render(request, self.template_name, data)

        try:
            state = States(**data_dict)
            state.full_clean()
            state.save()
        except:
            pass

        return redirect('states_list')


# states edit
class StatesEdit(UpdateView):
    model = States
    fields = '__all__'
    template_name = 'admin/states_form.html'

    def get_context_data(self, **kwargs):
        context = super(StatesEdit, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')
        context['lang'] = Languages.objects.filter(default=True).first()

        return context

    def form_valid(self, form):
        return None

    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, self.request)
        data = self.get_context_data()

        code = data_dict.get('code')
        codes = [str(it.code).lower() for it in States.objects.exclude(id=self.get_object().id)]
        
        if code is None:
            data['request_post'] = data_dict
            data['code_error'] = 'This field is required.'
            return render(request, self.template_name, data)
        elif str(code).lower() in codes:
            data['request_post'] = data_dict
            data['code_error'] = 'This code is already in use.'
            return render(request, self.template_name, data)

        if is_valid_field(data_dict, 'name') == False:
            data['request_post'] = data_dict
            data['error'] = 'This field is required.'
            return render(request, self.template_name, data)

        instance = self.get_object()

        for attr, value in data_dict.items():
            setattr(instance, attr, value)

        instance.save()

        return redirect('states_list')


# city list
class CityList(ListView):
    model = City
    template_name = 'admin/city_list.html'

    def get_queryset(self):
        queryset = City.objects.all()
        queryset = search(self.request, queryset, ['name'], self.model)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(CityList, self).get_context_data(**kwargs)

        context['objects'] = get_lst_data(self.get_queryset(), self.request, 20)
        context['page_obj'] = paginate(self.get_queryset(), self.request, 20)
        context['lang'] = Languages.objects.filter(active=True).filter(default=True).first()
        context['url'] = search_pagination(self.request)

        return context


# city create
class CityCreate(CreateView):
    model = City
    fields = '__all__'
    template_name = 'admin/city_form.html'

    def get_context_data(self, **kwargs):
        context = super(CityCreate, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')
        context['lang'] = Languages.objects.filter(default=True).first()
        context['states'] = States.objects.all()

        return context

    def form_valid(self, form):
        return None


    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, request)
        zip_codes = [it.zip for it in City.objects.all()]
        state_id = request.POST.get('state')
        data = self.get_context_data()

        if is_valid_field(data_dict, 'name') == False:
            data['request_post'] = data_dict
            data['name_error'] = 'This field is required.'
            return render(request, self.template_name, data)

        try:
            state = States.objects.get(id=int(state_id))
        except:
            state = None

        if state is None:
            data['request_post'] = data_dict
            data['state_error'] = 'This field is required.'
            return render(request, self.template_name, data)

        if data_dict.get('zip') is None:
            data['request_post'] = data_dict
            data['zip_error'] = 'This field is required.'
            return render(request, self.template_name, data)

        
        if data_dict.get('zip') in zip_codes:
            data['request_post'] = data_dict
            data['zip_error'] = 'This zip code is already in use.'
            return render(request, self.template_name, data)


        data_dict['state'] = state

        try:
            state = City(**data_dict)
            state.full_clean()
            state.save()
        except:
            pass

        return redirect('city_list')


# city edit
class CityEdit(UpdateView):
    model = City
    fields = '__all__'
    template_name = 'admin/city_form.html'


    def get_context_data(self, **kwargs):
        context = super(CityEdit, self).get_context_data(**kwargs)
        context['langs'] = Languages.objects.filter(active=True).order_by('-default')
        context['lang'] = Languages.objects.filter(default=True).first()
        context['states'] = States.objects.all()

        return context

    
    def form_valid(self, form):
        return None


    def post(self, request, *args, **kwargs):
        context = super().post(request, *args, **kwargs)
        data_dict = serialize_request(self.model, self.request)
        state_id = request.POST.get('state')
        zip_codes = [it.zip for it in City.objects.exclude(id=self.get_object().id)]
        data = self.get_context_data()

        try:
            state = States.objects.get(id=int(state_id))
        except:
            state = None

        if is_valid_field(data_dict, 'name') == False:
            data['request_post'] = data_dict
            data['error'] = 'This field is required.'
            return render(request, self.template_name, data)

        if state is None:
            data['request_post'] = data_dict
            data['state_error'] = 'This field is required.'
            return render(request, self.template_name, data)

        if data_dict.get('zip') is None:
            data['request_post'] = data_dict
            data['zip_error'] = 'This field is required.'
            return render(request, self.template_name, data)

        if data_dict.get('zip') in zip_codes:
            data['request_post'] = data_dict
            data['zip_error'] = 'This zip code is already in use.'
            return render(request, self.template_name, data)

        instance = self.get_object()
        data_dict['state'] = state

        for attr, value in data_dict.items():
            setattr(instance, attr, value)

        instance.save()

        return redirect('city_list')


# leads list
class LeadsList(ListView):
    model = Leads

    def get_queryset(self):
        queryset = Leads.objects.all()
        queryset = search(self.request, queryset, ['name'], self.model)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(LeadsList, self).get_context_data(**kwargs)

        context['objects'] = get_lst_data(self.get_queryset(), self.request, 20)
        context['page_obj'] = paginate(self.get_queryset(), self.request, 20)
        context['lang'] = Languages.objects.filter(active=True).filter(default=True).first()
        context['url'] = search_pagination(self.request)

        return context



# fill db view
def fill_db_view(request):
    if request.method == 'POST':
        if 'CITY' in request.POST:
            with open('admins/static/json/USCities.json') as f:
                j = json.load(f)
                zips = [str(it.zip) for it in City.objects.all()]

                for it in j:
                    try:
                        if str(it["zip_code"]).lower() not in zips:
                            state = States.objects.get(code=it['state'])
                            city = City.objects.create(
                                name = {"en": it["city"]},
                                state = state,
                                zip = it["zip_code"]
                            )
                            city.save()
                    except:
                        pass

        elif 'STATES' in request.POST:
            with open('/static/json/states_titlecase.json') as f:
                j = json.load(f)
                codes = [str(it.code).lower() for it in States.objects.all()]
                
                for it in j:
                    try:
                        if str(it["abbreviation"]).lower() not in codes:
                            state = States.objects.create(
                                name={"en": it['name']},
                                code=it['abbreviation']
                            )
                            state.save()
                    except:
                        pass


    return render(request, 'admin/fiil_db.html')





# logout
def logout_view(request):
    logout(request)

    return redirect('login_admin')
