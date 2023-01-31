from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required, user_passes_test



urlpatterns = [
    path('', views.home),
    path('articles', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.ArticlesList.as_view()), name='articles_list'),
    path('articles/create', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.ArticleCreateView.as_view()), name='articles_create'),
    path('articles/<int:pk>/edit', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.ArticleUpdate.as_view()), name='articles_edit'),
    path("article/delete", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.del_article), name='del_article'),
    path('langs', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.LangsList.as_view()), name='langs_list'),
    path('langs/create', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.LngCreateView.as_view()), name='create_lang'),
    path('langs/<int:pk>/edit', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.LangsUpdate.as_view()), name='lang_update'),
    path('langs/delete', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.delete_langs), name='lang_del'),
    path("site_infos", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.StaticUpdate.as_view()), name='static_info'),
    path('images/save', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.save_images), name='images_save'),
    path("images/delete", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.delete_image), name='del-img'),
    path("settings", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.FormSettings.as_view())),
    path('translations', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.TranslationList.as_view()), name='translation_list'),
    path("translations/<int:pk>", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.TranslationGroupDetail.as_view()), name='transl_group_detail'),
    path('translation/edit', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.translation_update), name='translation_edit'),
    path("translations/<int:pk>/edit", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.TranslationGroupUdpate.as_view()), name='transl_group_edit'),
    path("translation/delete", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.delete_translation), name='del_transl'),
    path("translation_group/create", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.add_trans_group), name='transl_group_create'),
    path('article_categories', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.ArticleCtgList.as_view()), name='article_ctg_list'),
    path('article_categories/create', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.AddArticleCtg.as_view()), name='add_acticle_ctg'),
    path("article_categories/<int:pk>/edit", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.ArticleCtgEdit.as_view()), name='article_ctg_update'),
    path('article_categories/delete', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.article_ctg_del), name='del_art_ctg'),
    path("faq", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.FAQlist.as_view()), name='faq_list'),
    path("faq/create", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.FAQcreate.as_view()), name='faq_create'),
    path('faq/<int:pk>/edit', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.FAQupdate.as_view()), name='faq_edit'),
    path("events", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.EventsList.as_view()), name='events_list'),
    path('events/create', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.EventsCreate.as_view()), name="events_create"),
    path("events/<int:pk>/edit", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.EventsUpdate.as_view()), name='events_update'),
    path("delete", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.delete_item), name='delete'),
    path('delete_alot', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.delete_alot), name='del_alot'),
    path("lang_icon_delete", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.del_lang_icon), name='lang_icon_del'),
    path("add_static_image", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.add_static_image), name='add_static_logos'),
    path("delete_static_image", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.del_statics_image), name='del_static_image'),
    path('delete_article_ctg_images', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.delete_article_group_img), name='art_ctg_image_del'),
    path("about_us", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.AboutUsView.as_view()), name='about_us'),
    path("about_us/video/delete", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.delete_about_video), name='del_about_video'),
    path('about_us/video/set', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.set_about_video), name='set_about_video'),
    path('services', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.ServicesList.as_view()), name='services'),
    path("services/create", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.ServiceCreate.as_view()), name='services_create'),
    path("services/<int:pk>/edit", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.ServicesUpdate.as_view()), name='services_update'),
    path("delete_service_image", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.del_sev_image), name='del_serv_image'),
    path('login', LoginView.as_view(
        template_name='admin/sing-in.html',
        success_url='/admin/',
    ), name = 'login_admin'),
    path('admins', user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.AdminsList.as_view()), name='admin_list'),
    path("admins/create", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.AdminCreate.as_view()), name='admins_create'),
    path("admins/<int:pk>/edit", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.AdminUpdate.as_view()), name='admins_edit'),
    path("delete_article_image", user_passes_test(lambda u: u.is_superuser, login_url='login_admin')(views.delete_article_image), name='del_article_img')
]
