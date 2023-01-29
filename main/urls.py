from django.urls import path, include
from . import views


urlpatterns = [
    path('articles', views.ArticlesList.as_view()),
    path("articles/<int:pk>", views.ArticlesDetail.as_view()),
    path('services', views.ServicesListView.as_view()),
    path("services/<int:pk>", views.ServicesDetailView.as_view()),
    path('about_us', views.AboutUsView.as_view()),
    path("static_infos", views.StaticInfView.as_view()),
    path("translations", views.TranslationsView.as_view())
]