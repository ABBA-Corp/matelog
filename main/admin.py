from django.contrib import admin
from .models import City, States, Leads
# Register your models here.


admin.site.register(City)
admin.site.register(States)


class LeadsAdmin(admin.ModelAdmin):
    list_display = [it.name for it in Leads._meta.fields]

    class Meta:
        models = Leads


admin.site.register(Leads, LeadsAdmin)