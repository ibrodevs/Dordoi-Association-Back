from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.
class Partner(models.Model):
    logo = models.ImageField(upload_to="partners/logos/", verbose_name="Логотип", null=True, blank=True)
    name_en = models.CharField(max_length=255, verbose_name="Название (EN)")
    name_ru = models.CharField(max_length=255, verbose_name="Название (RU)")
    name_kg = models.CharField(max_length=255, verbose_name="Название (KG)")
    description_ru = CKEditor5Field(
        "Description (RU)", config_name="extends", null=True, blank=True
    )
    description_en = CKEditor5Field(
        "Description (EN)", config_name="extends", null=True, blank=True
    )
    description_kg = CKEditor5Field(
        "Description (KG)", config_name="extends", null=True, blank=True
    )

    coord1 = models.CharField(max_length=55, verbose_name='координаты ширины(LAT)', null=True, blank=True)
    coord2 = models.CharField(max_length=55, verbose_name='координаты долготы(LMG)', null=True, blank=True)

    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"
        ordering = ["id"]   
    def __str__(self):
        return self.get_name()
    def get_name(self, language="ru"):
        return getattr(self, f"name_{language}", self.name_ru)
    def get_description(self, language="ru"):
        return getattr(self, f"description_{language}", self.description_ru)





class Category(models.Model):

    title_en = models.CharField(max_length=255, verbose_name="Название (EN)")
    title_ru = models.CharField(max_length=255, verbose_name="Название (RU)")
    title_kg = models.CharField(max_length=255, verbose_name="Название (KG)")

    class Meta:
        verbose_name = "Категория для проектов"
        verbose_name_plural = "Категории для проектов"

    def __str__(self):
        return self.get_title()

    def get_title(self, language="ru"):
        return getattr(self, f'title_{language}', self.title_ru)

class Projects(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
        verbose_name="Категория",
    )


    title_en = models.CharField(max_length=255, verbose_name="Заголовок (EN)")
    title_ru = models.CharField(max_length=255, verbose_name="Заголовок (RU)")
    title_kg = models.CharField(max_length=255, verbose_name="Заголовок (KG)")

    short_description_en = models.TextField(
        blank=True,
        verbose_name="Краткое описание (EN)",
    )
    short_description_ru = models.TextField(
        blank=True,
        verbose_name="Краткое описание (RU)",
    )
    short_description_kg = models.TextField(
        blank=True,
        verbose_name="Краткое описание (KG)",
    )

    description_en = models.TextField(blank=True, verbose_name="Описание (EN)")
    description_ru = models.TextField(blank=True, verbose_name="Описание (RU)")
    description_kg = models.TextField(blank=True, verbose_name="Описание (KG)")

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания", db_index=True
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    published_at = models.DateField(
        null=True, blank=True, verbose_name="Дата публикации", db_index=True
    )

    image = models.ImageField(
        upload_to="news/",
        null=True,
        blank=True,
        verbose_name="Изображение",
        help_text="Рекомендуемый размер: (16:9)",
    )

    cropping = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Обрезка изображения",
        help_text="Координаты обрезки изображения (JSON формат)",
    )

    class Meta:
        verbose_name = "проект"
        verbose_name_plural = "проекты"

    def __str__(self):
        return self.get_title()

    def get_title(self, language="ru"):
        field_name = f"title_{language}"
        value = getattr(self, field_name, None)

        if value and value.strip():
            return value.strip()

        if language != "ru" and self.title_ru and self.title_ru.strip():
            return self.title_ru.strip()

        if language != "en" and self.title_en and self.title_en.strip():
            return self.title_en.strip()

        return f"News #{self.pk}" if self.pk else "New News"

    def get_description(self, language="ru"):
        field_name = f"description_{language}"
        value = getattr(self, field_name, None)

        if value and value.strip():
            return value.strip()

        if language != "ru" and self.description_ru and self.description_ru.strip():
            return self.description_ru.strip()

        if language != "en" and self.description_en and self.description_en.strip():
            return self.description_en.strip()

        return ""

    def get_short_description(self, language="ru"):
        field_name = f"short_description_{language}"
        value = getattr(self, field_name, None)

        if value and value.strip():
            return value.strip()

        if (
            language != "ru"
            and self.short_description_ru
            and self.short_description_ru.strip()
        ):
            return self.short_description_ru.strip()

        if (
            language != "en"
            and self.short_description_en
            and self.short_description_en.strip()
        ):
            return self.short_description_en.strip()

        return self.get_description(language)






