from unfold.admin import ModelAdmin
from django.contrib import admin
from .models import Partner, Projects, ProjectGallery


@admin.register(Partner)
class PartnerAdmin(ModelAdmin):
    pass

class ProjectGalleryAdmin(admin.TabularInline):
    model=ProjectGallery
    extra = 2


@admin.register(Projects)
class ProjectsAdmin(ModelAdmin):
    inlines = [ProjectGalleryAdmin]



