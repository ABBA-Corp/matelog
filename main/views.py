from django.shortcuts import render
from rest_framework import views, generics
from .serializers import ArticleSerializer, ServiceSerializer, AboutUsSerializer, StaticInformationSerializer, TranslationSerializer, LangsSerializer
from admins.models import Articles, Languages, Translations, Services, AboutUs, StaticInformation
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import CarMarks, CarsModel, States, City
from .serializers import CarMarkSerializer, CarModelSerializer
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
    queryset = Services.objects.all()
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
        obj = StaticInformation.objects.first()

        if not obj:
            return Response({'detail': 'There is no About Us information'})

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
        mark_id = self.request.data.get('make', '')

        if mark_id != '':
            try:
                mark = CarMarks.objects.get(id=int(mark_id))
                queryset = queryset.filter(mark=mark)
            except:
                pass

        return queryset





    