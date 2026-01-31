from unfold.admin import ModelAdmin
from django.contrib import admin
from .models import Partner, Projects, Category


@admin.register(Partner)
class PartnerAdmin(ModelAdmin):
    pass



@admin.register(Projects)
class ProjectsAdmin(ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    pass

