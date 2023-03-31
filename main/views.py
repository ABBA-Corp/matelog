from django.shortcuts import render
from rest_framework import views, generics
from .serializers import ArticleSerializer, ServiceSerializer, AboutUsSerializer, StaticInformationSerializer, TranslationSerializer, LangsSerializer
from .serializers import NewAplSerializer
from admins.models import Articles, Languages, Translations, Services, AboutUs, StaticInformation, Reviews
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import CarMarks, CarsModel, States, City, Leads, Applications, AplicationNbm, ShortApplication, SomeAplication
import requests
import json
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from .serializers import CarMarkSerializer, CarModelSerializer, CitySimpleSerializer, CitySerializer, StateSerializer, LeadsCreateSerialzier, LeadsViewSerializer, ApplicationCreateSerializer, ReviewSerializer, ShortApplicationSerializer
from django.template.loader import get_template
from django.db.models import Q
# Create your views here.

# pagination
class BasePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


# articles list
class ArticlesList(generics.ListAPIView):
    queryset = Articles.objects.filter(active=True)
    serializer_class = ArticleSerializer
    pagination_class = BasePagination


# articles detail
class ArticlesDetail(generics.RetrieveAPIView):
    queryset = Articles.objects.filter(active=True)
    serializer_class = ArticleSerializer


# service view
class ServicesListView(generics.ListAPIView):
    queryset = Services.objects.order_by("order")
    serializer_class = ServiceSerializer
    pagination_class = BasePagination


# servise detail view
class ServicesDetailView(generics.RetrieveAPIView):
    queryset = Services.objects.all()
    serializer_class = ServiceSerializer



# about us 
class AboutUsView(views.APIView):
    def get(self, request, format=None):
        obj = AboutUs.objects.first()

        if not obj:
            return Response({'detail': 'There is no About Us information'})

        serializer = AboutUsSerializer(obj, context={'request': request})
        
        return Response(serializer.data)



# static information
class StaticInfView(views.APIView):
    def get(self, request, format=None):
        try:
            obj = StaticInformation.objects.get(id=1)
        except:
            obj = StaticInformation.objects.create()

        serializer = StaticInformationSerializer(obj, context={'request': request})

        return Response(serializer.data)



# translations
class TranslationsView(views.APIView):
    def get(self, request, fromat=None):
        translations = Translations.objects.all()
        serializer = TranslationSerializer(translations, context={'request': request})
        return Response(serializer.data)


# langs list
class LangsList(generics.ListAPIView):
    queryset = Languages.objects.filter(active=True)
    serializer_class = LangsSerializer
    pagination_class = BasePagination



# car mark list
class CarMarkList(generics.ListAPIView):
    queryset = CarMarks.objects.all()
    serializer_class = CarMarkSerializer
    pagination_class = BasePagination


# car models list
class CarModelsList(generics.ListAPIView):
    serializer_class = CarModelSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        queryset = CarsModel.objects.all()
        mark_id = self.request.GET.get('make', '')

        if mark_id != '':
            try:
                mark = CarMarks.objects.get(id=int(mark_id))
                queryset = queryset.filter(mark=mark)
            except:
                pass

        return queryset




# state view
class StatesList(generics.ListAPIView):
    queryset = States.objects.all()
    serializer_class = StateSerializer
    pagination_class = BasePagination


    def get_queryset(self):
        queryset = self.queryset
        query = self.request.GET.get("q", '')

        if query != '':
            queryset = queryset.extra(where=[f'LOWER(name ::varchar) LIKE %s'], params=[f'%{query.lower()}%'])

        return queryset
    


# city list
class CityList(generics.ListAPIView):
    serializer_class  = CitySimpleSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        queryset = City.objects.all()
        state_id = self.request.GET.get('state', '')
        query = self.request.GET.get("q", '')

        if state_id != '':
            try:
                state = States.objects.get(id=int(state_id))
                queryset = queryset.filter(state=state)
            except:
                pass

        
        if query != '':
            queryset = queryset.filter(Q(name__iregex=query) | Q(zip__iregex=query))

        
        return queryset


# city detail
class CityDetailView(generics.RetrieveAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.all()




# lead create
class LeadCreate(generics.CreateAPIView):
    queryset = Leads.objects.all()
    serializer_class = LeadsCreateSerialzier


    def perform_create(self, serializer):
        lead = serializer.save()

        html_templ = get_template('email.html')
        lang = Languages.objects.filter(default=True).first()

        try:
            subject = 'hello'
            text_content = 'some'
            html_content = html_templ.render(context={'lead': lead, 'lang': lang})
            msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [lead.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except:
            pass

        return lead


# leads detail view
class LeadDetailView(generics.RetrieveAPIView):
    queryset = Leads.objects.all()
    lookup_field = 'uuid'
    serializer_class = LeadsViewSerializer


# lead update view
class LeadUpdateView(generics.UpdateAPIView):
    queryset = Leads.objects.all()
    lookup_field = 'uuid'
    serializer_class = LeadsCreateSerialzier



# aplication create view
class ApplicationCreateView(generics.CreateAPIView):
    queryset = Applications.objects.all()
    serializer_class = ApplicationCreateSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            apl = serializer.save()
            nbms = list(self.request.data.get('nbms', []))

            for nbm in nbms:
                AplicationNbm(application=apl, nbm=nbm).save()

            html_templ = get_template('application_email.html')
            lang = Languages.objects.filter(default=True).first()

            try:
                subject = 'Your application'
                text_content = 'some'
                html_content = html_templ.render(context={'apl': apl, 'lang': lang})
                msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [apl.email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except:
                pass

        return apl


    def post(self, request, *args, **kwargs):
        lead_id = self.request.data.get('lead')
        try:
            Leads.objects.get(id=lead_id)
        except:
            return Response({'error': 'Lead id is invalid'})

        nbms = self.request.data.get('nbms', [])

        if type(nbms) != list:
            return Response({'TypeError': 'nbms param should be list not {}'.format(type(nbms).__name__)})

        
        contact_me = request.data.get('contact_me', False)
        contact_else = request.data.get('contact_else', '')

        if not contact_me and contact_else == '':
            return Response({'error': 'contact_else is required if contact_me is False'})

        return super().post(request, *args, **kwargs)


# reviews list
class ReviewList(generics.ListAPIView):
    queryset = Reviews.objects.filter(active=True)
    serializer_class = ReviewSerializer
    pagination_class = BasePagination


# create short application view
class ShortAplicationView(generics.CreateAPIView):
    queryset = ShortApplication.objects.all()
    serializer_class = ShortApplicationSerializer
    fields = '__all__'



# add application (sory if you read this)
class NewAmgAplication(generics.CreateAPIView):
    queryset = SomeAplication.objects.all()
    serializer_class = NewAplSerializer



# get order status
class GetOrderStatus(views.APIView):
    def get(self, request, format=None):

        data = {
            'api_key': settings.SRM_API_KEY
        }

        data['record'] = request.GET.get("record", '')

        response = requests.get(url='https://ml.msgplane.com/api/rest/get/status/', params=data)
        response_data = response.json()

        if 'result' in response_data and response_data['result'] == 'failed':
            return Response(status=403, data=response.json())

        status_dict = {
            '100': 'new',
            '1': 'follow-up',
            '2': 'cancelled',
            '20': 'on-hold-lead',
            '21': 'on-hold-quote',
            '3': 'quote',
            '4': 'order',
            '5': 'signed',
            '30': 'on-hold-quote',
            '60': 'ready',
            '61': 'bounced',
            '7': 'posted-cd',
            '8': 'dispatched',
            '80': 'not-signed',
            '81': 'picked-up',
            '9': 'on-hold-order',
            '10': 'completed',
            '11': 'incomplete',
            '12': 'lost',
            '13': 'cancelled',
            '999': 'archived',
            '888': 'bad',

        }

        response_data['status'] = status_dict.get(response_data['lead_status'], 'ERROR')

        return Response(response_data)
