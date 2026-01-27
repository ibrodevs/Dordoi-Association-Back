from django.db import models
from django.core.exceptions import ValidationError
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.


class FactCard(models.Model):
    # is_banner = models.BooleanField(default=False, verbose_name="Является баннером?")
    is_banner = models.BooleanField(default=False, verbose_name="Является баннером?")

    photo = models.ImageField(
        upload_to="fact_cards/",
        verbose_name="Фото",
        blank=True,
        null=True,
    )

    title_en = models.CharField(max_length=255, verbose_name="Заголовок (EN)")
    title_ru = models.CharField(max_length=255, verbose_name="Заголовок (RU)")
    title_kg = models.CharField(max_length=255, verbose_name="Заголовок (KG)")

    description_en = models.TextField(verbose_name="Описание (EN)")
    description_ru = models.TextField(verbose_name="Описание (RU)")
    description_kg = models.TextField(verbose_name="Описание (KG)")

    class Meta:
        verbose_name = "Факт-карта"
        verbose_name_plural = "Факт-карты"
        ordering = ["id"]

    def clean(self):
        if self.is_banner and not self.photo:
            raise ValidationError("Для баннеров обязательно нужно загрузить фото.")

    def __str__(self):
        return self.get_title()

    def get_title(self, language="ru"):
        return getattr(self, f"title_{language}", self.title_ru)

    def get_description(self, language="ru"):
        return getattr(self, f"description_{language}", self.description_ru)


class Leader(models.Model):
    photo = models.ImageField(upload_to="leaders/", verbose_name="Фото")
    name_ru = models.CharField(max_length=255, verbose_name="ФИО (RU)")
    name_en = models.CharField(max_length=255, verbose_name="ФИО (EN)")
    name_kg = models.CharField(max_length=255, verbose_name="ФИО (KG)")
    position_ru = models.CharField(max_length=255, verbose_name="Должность (RU)")
    position_en = models.CharField(max_length=255, verbose_name="Должность (EN)")
    position_kg = models.CharField(max_length=255, verbose_name="Должность (KG)")
    bio_kg = models.TextField(
        verbose_name="Биография (KG) - необязательно заполнять", blank=True, null=True
    )
    bio_ru = models.TextField(
        verbose_name="Биография (RU) - необязательно заполнять", blank=True, null=True
    )
    bio_en = models.TextField(
        verbose_name="Биография (EN) - необязательно заполнять", blank=True, null=True
    )
    achievements_kg = models.JSONField(
        verbose_name="Достижения (KG) - необязательно заполнять",
        default=list,
        blank=True,
        null=True,
    )
    achievements_ru = models.JSONField(
        verbose_name="Достижения (RU) - необязательно заполнять",
        default=list,
        blank=True,
        null=True,
    )
    achievements_en = models.JSONField(
        verbose_name="Достижения (EN) - необязательно заполнять",
        default=list,
        blank=True,
        null=True,
    )
    education_kg = models.JSONField(
        verbose_name="Образование (KG) - необязательно заполнять",
        default=list,
        blank=True,
        null=True,
    )
    education_ru = models.JSONField(
        verbose_name="Образование (RU) - необязательно заполнять",
        default=list,
        blank=True,
        null=True,
    )
    education_en = models.JSONField(
        verbose_name="Образование (EN) - необязательно заполнять",
        default=list,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Руководитель"
        verbose_name_plural = "Руководство"
        ordering = ["id"]

    def __str__(self):
        return self.get_name()

    def get_name(self, language="ru"):
        return getattr(self, f"name_{language}", self.name_ru)

    def get_position(self, language="ru"):
        return getattr(self, f"position_{language}", self.position_ru)

    def get_bio(self, language="ru"):
        return getattr(self, f"bio_{language}", self.bio_ru)

    def get_achievements(self, language="ru"):
        return getattr(self, f"achievements_{language}", self.achievements_ru)

    def get_education(self, language="ru"):
        return getattr(self, f"education_{language}", self.education_ru)


# history section
class History(models.Model):

    description_ru = models.TextField()
    description_en = models.TextField()
    description_kg = models.TextField()

    image = models.ImageField(upload_to="history/", blank=True, null=True)

    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Историческая веха"
        verbose_name_plural = "История"

    def __str__(self):
        return f"{self.order}. {self.description_ru[:50]}..."

    def get_description(self, language="ru"):
        return getattr(self, f"description_{language}", self.description_ru)


class CategoryStructure(models.Model):
    name_kg = models.CharField(max_length=255, unique=True, verbose_name="название на кыргызском")
    name_en = models.CharField(max_length=255, unique=True, verbose_name="название на английском")
    name_ru = models.CharField(max_length=255, unique=True, verbose_name="название на русском")

    class Meta:
        verbose_name = 'категория для структур'
        verbose_name_plural = 'категории для структур'

    def __str__(self):
        return self.name_ru

    def get_name(self, language):
        return getattr(self, f'name_{language}', self.name_ru)

class Structure(models.Model):
    """
    Структурные подразделения ассоциации
    """

    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug (URL)")

    category = models.ForeignKey(CategoryStructure, verbose_name='категория', null=True, blank=True, on_delete=models.SET_NULL)

    logo = models.ImageField(upload_to="subsidiaries/logos/", verbose_name="Логотип")

    aspect_ratio = models.CharField(
        choices=[
            ("square", "Квадрат (1:1)"),
            ("portrait", "Портрет (3:4)"),
            ("landscape", "Пейзаж (4:3)"),
            ("wide", "Широкий (16:9)"),
            ("tall", "Высокий (9:16)"),
        ],
        default="square",
        max_length=20,
        verbose_name="Пропорции логотипа",
    )

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

    address_kg = models.CharField(max_length=500,  blank=True, verbose_name='адрес на кыргызском')
    address_ru = models.CharField(max_length=500,  blank=True, verbose_name='адрес на русском ')
    address_en = models.CharField(max_length=500, blank=True, verbose_name='адрес на английском')

    email = models.EmailField(verbose_name="Email", blank=True)
    phone = models.CharField(max_length=50, verbose_name="Телефон", blank=True)

    order = models.IntegerField(default=0, verbose_name="Порядок отображения")

    class Meta:
        verbose_name = "Структурное подразделение"
        verbose_name_plural = "Структура"
        ordering = ["order", "name_ru"]

    def __str__(self):
        return self.get_name()

    def get_name(self, language="ru"):
        field_name = f"name_{language}"
        return getattr(self, field_name, self.name_ru)

    def get_description(self, language="ru"):
        field_name = f"description_{language}"
        return getattr(self, field_name, self.description_ru)

    def get_address(self, language='ru'):
        return getattr(self, f'address_{language}', self.address_ru)
