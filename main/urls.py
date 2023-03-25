from django.urls import path, include
from . import views


urlpatterns = [
    path('articles', views.ArticlesList.as_view()),
    path("articles/<int:pk>", views.ArticlesDetail.as_view()),
    path('services', views.ServicesListView.as_view()),
    path("services/<int:pk>", views.ServicesDetailView.as_view()),
    path('about_us', views.AboutUsView.as_view()),
    path("static_infos", views.StaticInfView.as_view()),
    path("translations", views.TranslationsView.as_view()),
    path('languages', views.LangsList.as_view()),
    path("car_makes", views.CarMarkList.as_view()),
    path("car_models", views.CarModelsList.as_view()),
    path("states", views.StatesList.as_view()),
    path('cities', views.CityList.as_view()),
    path('city/<int:pk>', views.CityDetailView.as_view()),
    path("leads/create", views.LeadCreate.as_view()),
    path("leads/<uuid:uuid>", views.LeadDetailView.as_view()),
    path('leads/<uuid:uuid>/edit', views.LeadUpdateView.as_view()),
    path("applications/create", views.ApplicationCreateView.as_view()),
    path('reviews', views.ReviewList.as_view()),
    path('short_application/create', views.ShortAplicationView.as_view()),
    path('application/create', views.NewAmgAplication.as_view()),
    path("get_order_status", views.GetOrderStatus.as_view())
]