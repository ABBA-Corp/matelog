from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required, user_passes_test


urlpatterns = [
    path('', views.home, name='home'),
    path('articles', views.ArticlesList.as_view(), name='articles_list'),
    path('articles/create', views.ArticleCreateView.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit', views.ArticleUpdate.as_view(), name='articles_edit'),
    path("article/delete", views.del_article, name='del_article'),
    path('langs', views.LangsList.as_view(), name='langs_list'),
    path('langs/create', views.LngCreateView.as_view(), name='create_lang'),
    path('langs/<int:pk>/edit', views.LangsUpdate.as_view(), name='lang_update'),
    path('langs/delete', views.delete_langs, name='lang_del'),
    path("site_infos", views.StaticUpdate.as_view(), name='static_info'),
    path('images/save', views.save_images, name='images_save'),
    path("images/delete", views.delete_image, name='del-img'),
    path('translations', views.TranslationList.as_view(), name='translation_list'),
    path("translations/<int:pk>", views.TranslationGroupDetail.as_view(), name='transl_group_detail'),
    path('translation/edit', views.translation_update, name='translation_edit'),
    path("translations/<int:pk>/edit", views.TranslationGroupUdpate.as_view(), name='transl_group_edit'),
    path("translation/delete", views.delete_translation, name='del_transl'),
    path("translation_group/create", views.add_trans_group, name='transl_group_create'),
    path('article_categories', views.ArticleCtgList.as_view(), name='article_ctg_list'),
    path('article_categories/create', views.AddArticleCtg.as_view(), name='add_acticle_ctg'),
    path("article_categories/<int:pk>/edit", views.ArticleCtgEdit.as_view(), name='article_ctg_update'),
    path('article_categories/delete', views.article_ctg_del, name='del_art_ctg'),
    path("delete", views.delete_item, name='delete'),
    path('delete_alot', views.delete_alot, name='del_alot'),
    path("lang_icon_delete", views.del_lang_icon, name='lang_icon_del'),
    path("add_static_image", views.add_static_image, name='add_static_logos'),
    path("delete_static_image", views.del_statics_image, name='del_static_image'),
    path('delete_article_ctg_images', views.delete_article_group_img, name='art_ctg_image_del'),
    path("about_us", views.AboutUsView.as_view(), name='about_us'),
    path("about_us/video/delete", views.delete_about_video, name='del_about_video'),
    path('about_us/video/set', views.set_about_video, name='set_about_video'),
    path('services', views.ServicesList.as_view(), name='services'),
    path("services/create", views.ServiceCreate.as_view(), name='services_create'),
    path("services/<int:pk>/edit", views.ServicesUpdate.as_view(), name='services_update'),
    path("delete_service_image", views.del_sev_image, name='del_serv_image'),
    path('login', LoginView.as_view(
        template_name='admin/sing-in.html',
        success_url='/admin/',
    ), name='login_admin'),
    path('logout', views.logout_view, name='logout_url'),
    path('admins', views.AdminsList.as_view(), name='admin_list'),
    path("admins/create", views.AdminCreate.as_view(), name='admins_create'),
    path("admins/<int:pk>/edit", views.AdminUpdate.as_view(), name='admins_edit'),
    path("delete_article_image", views.delete_article_image, name='del_article_img'),
    path('car_makes', views.CarMarkList.as_view(), name='car_makes_list'),
    path("car_makes/create", views.CarMarkCreate.as_view(), name='car_makes_create'),
    path("car_makes/<int:pk>/edit", views.CarMarkEdit.as_view(), name='car_makes_edit'),
    path('car_models', views.CarsModelList.as_view(), name='car_models'),
    path("car_models/create", views.CarModelCreate.as_view(), name='car_models_create'),
    path("car_models/<int:pk>/edit", views.CarModelEdit.as_view(), name="car_models_edit"),
    path("city", views.CityList.as_view(), name='city_list'),
    path('city/create', views.CityCreate.as_view(), name='city_create'),
    path("city/<int:pk>/edit", views.CityEdit.as_view(), name='city_edit'),
    path('states', views.StatesList.as_view(), name='states_list'),
    path('states/create', views.StatesCreate.as_view(), name='states_create'),
    path('states/<int:pk>/edit', views.StatesEdit.as_view(), name='state_edit'),
    path("applications", views.ApplicationsList.as_view(), name='appl_list'),
    path('applications/<int:pk>', views.ApplicationDetailView.as_view(), name='apl_view'),
    path('applications/<int:pk>/edit', views.ApplicationUpdate.as_view(), name='apl_edit'),
    path("reviews", views.ReviewsList.as_view(), name='review_list'),
    path("reviews/create", views.ReviewsCreate.as_view(), name='review_create'),
    path('reviews/<int:pk>/edit', views.ReviewsUpdate.as_view(), name='review_edit'),
    path('delete_review_image', views.delete_review_image, name='del_review_image'),
    path('quick_applications', views.ShortApplicationList.as_view(), name='short_aplic_list'),
    path('quick_applications/<int:pk>/edit', views.ShortApplicationUpdate.as_view(), name='short_aplic_edit'),
    path("contacts", views.AmigaSkiAplicationList.as_view(), name='contacts_list'),
    path("contacts/<int:pk>", views.NewAplDetail.as_view(), name='contacts_detail'),

    path("fill_db_qwertyuiop", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.fill_db_view))
]
