from unfold.admin import ModelAdmin
from django.contrib import admin
from .models import Category, News, Publication, NewsPhoto


class NewsPhotoInline(admin.TabularInline):
    model = NewsPhoto
    extra = 1
    fields = ['image', 'order']
    ordering = ['order']


@admin.register(Publication)
class PublicationAdmin(ModelAdmin):
    pass
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ["id", "get_title_ru"]
    search_fields = ["title_ru", "title_en", "title_kg"]

    fieldsets = (
        ("Название", {"fields": ("title_ru", "title_en", "title_kg")}),
    )

    def get_title_ru(self, obj):
        return obj.title_ru

    get_title_ru.short_description = "Название (RU)"


@admin.register(News)
class NewsAdmin(ModelAdmin):
    inlines = [NewsPhotoInline]
    list_display = ["id", "get_title_ru", "category", "is_banner", "is_recommended", "published_at", "created_at"]
    search_fields = ["title_ru", "title_en", "title_kg", "description_ru"]
    readonly_fields = ["created_at", "updated_at"]
    list_filter = ["category", "is_banner", "is_recommended", "published_at"]
    list_editable = ["is_banner", "is_recommended"]

    fieldsets = (
        ("Основная информация", {
            "fields": ("title_ru", "title_en", "title_kg", "category", "is_banner", "is_recommended")
        }),
        ("Краткое описание", {
            "fields": ("short_description_ru", "short_description_en", "short_description_kg")
        }),
        ("Полное описание", {
            "fields": ("description_ru", "description_en", "description_kg")
        }),
        ("Изображение", {
            "fields": ("image", "cropping")
        }),
        ("Публикация", {
            "fields": ("published_at",)
        }),
        ("Даты", {
            "fields": ("created_at", "updated_at")
        }),
    )

    def get_title_ru(self, obj):
        return obj.title_ru

    get_title_ru.short_description = "Заголовок (RU)"


@admin.register(NewsPhoto)
class NewsPhotoAdmin(ModelAdmin):
    list_display = ["id", "news", "order"]
    search_fields = ["news__title_ru"]
    list_filter = ["news"]

    fieldsets = (
        ("Новость", {"fields": ("news",)}),
        ("Изображение", {"fields": ("image", "order")}),
    )
