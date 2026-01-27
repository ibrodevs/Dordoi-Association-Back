from unfold.admin import ModelAdmin
from django.contrib import admin
from .models import FactCard, Leader, History, Structure, CategoryStructure


@admin.register(FactCard)
class FactCardAdmin(ModelAdmin):
    fieldsets = (
        ("Основное", {"fields": ("is_banner",)}),
        (
            "Фото",
            {
                "fields": ("photo",),
                "description": "Фото обязательно для баннеров. Для обычных фактов можно оставить пустым.",
            },
        ),
        ("Заголовок", {"fields": ("title_en", "title_ru", "title_kg")}),
        (
            "Описание",
            {"fields": ("description_en", "description_ru", "description_kg")},
        ),
    )


@admin.register(Leader)
class LeaderAdmin(ModelAdmin):
    pass


@admin.register(History)
class HistoryAdmin(ModelAdmin):
    list_display = ["order", "get_short_description"]
    list_display_links = ["get_short_description"]
    list_editable = ["order"]
    ordering = ["order"]

    fieldsets = (
        ("Порядок", {"fields": ("order",)}),
        ("Изображение", {"fields": ("image",)}),
        (
            "Описание",
            {"fields": ("description_ru", "description_en", "description_kg")},
        ),
    )

    def get_short_description(self, obj):
        return (
            obj.description_ru[:50] + "..."
            if len(obj.description_ru) > 50
            else obj.description_ru
        )

    get_short_description.short_description = "Описание (RU)"


@admin.register(Structure)
class StructureAdmin(ModelAdmin):
    pass

@admin.register(CategoryStructure)
class CategoryStructureAdmin(ModelAdmin):
    pass