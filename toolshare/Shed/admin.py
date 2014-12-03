from django.contrib import admin
from Shed.models import Shed

class ShedAdmin(admin.ModelAdmin):
    list_display = ('shed_Name', 'Zip_Code', 'City', 'State', 'Shed_Owner')

admin.site.register(Shed, ShedAdmin)