from django.contrib import admin
from Tool.models import Tool

# Register your models here.

class ToolAdmin(admin.ModelAdmin):
    list_display = ('toolname','description','shared')

admin.site.register(Tool, ToolAdmin)