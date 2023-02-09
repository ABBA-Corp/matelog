from django.contrib import admin
from .models import StaticInformation, ImageGalery, VideoGalery, TranlsationGroups, Articles, Languages, Translations, FAQ, AdminInputs, ArticleCategories, ArticleImages, Services, MetaTags, Reviews
from django.contrib.auth.models import Permission
# Register your models here.



admin.site.register(StaticInformation)
admin.site.register(ImageGalery)
admin.site.register(VideoGalery)
admin.site.register(Translations)
admin.site.register(TranlsationGroups)
admin.site.register(Languages)
admin.site.register(Articles)
admin.site.register(FAQ)
admin.site.register(AdminInputs)
admin.site.register(ArticleCategories)
admin.site.register(ArticleImages)
admin.site.register(Services)
admin.site.register(MetaTags)
admin.site.register(Permission)
admin.site.register(Reviews)