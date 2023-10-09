from django.contrib import admin
from .models import *


class ImageInline(admin.TabularInline):
    model = ProjectImages
    extra = 1  # Number of empty forms to display

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ImageInline]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Article)
admin.site.register(Settings)
admin.site.register(Batch)
admin.site.register(ReviewLogs)