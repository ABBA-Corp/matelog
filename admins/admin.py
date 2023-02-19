from django.contrib import admin
from .models import StaticInformation, TranlsationGroups, Articles, Languages, Translations, AdminInputs, ArticleCategories, ArticleImages, Services, MetaTags, Reviews
from django.contrib.auth.models import Permission
# Register your models here.



admin.site.register(StaticInformation)
admin.site.register(Translations)
admin.site.register(TranlsationGroups)
admin.site.register(Languages)
admin.site.register(Articles)
admin.site.register(AdminInputs)
admin.site.register(ArticleCategories)
admin.site.register(ArticleImages)
admin.site.register(Services)
admin.site.register(MetaTags)
admin.site.register(Permission)
admin.site.register(Reviews)