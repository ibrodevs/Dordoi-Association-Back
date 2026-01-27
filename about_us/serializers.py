from rest_framework import serializers
from .models import FactCard, Leader, History, Structure


class LeaderSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    position = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()
    achievements = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()

    class Meta:
        model = Leader
        fields = ["id", "photo", "name", "position", "bio", "achievements", "education"]

    def get_name(self, obj):
        return obj.get_name(self.context.get("language", "ru"))

    def get_position(self, obj):
        return obj.get_position(self.context.get("language", "ru"))

    def get_bio(self, obj):
        return obj.get_bio(self.context.get("language", "ru"))

    def get_achievements(self, obj):
        return obj.get_achievements(self.context.get("language", "ru"))

    def get_education(self, obj):
        return obj.get_education(self.context.get("language", "ru"))


class LocalizationSerializerMixin:
    """Миксин для локализации сериализаторов"""

    def _get_language(self):
        lang = self.context.get("language")
        if lang:
            return lang
        request = self.context.get("request")
        if request:
            return (
                request.GET.get("lang")
                or getattr(request, "LANGUAGE_CODE", None)
                or "ru"
            )
        return "ru"


class FactCardSerializer(LocalizationSerializerMixin, serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = FactCard
        fields = ["id", "photo", "title", "description", "is_banner"]
        read_only_fields = ["id"]

    def get_title(self, obj):
        language = self._get_language()
        return obj.get_title(language=language)

    def get_description(self, obj):
        language = self._get_language()
        field_name = f"description_{language}"
        value = getattr(obj, field_name, None)

        if value and value.strip():
            return value.strip()

        if language != "ru" and obj.description_ru and obj.description_ru.strip():
            return obj.description_ru.strip()

        if language != "en" and obj.description_en and obj.description_en.strip():
            return obj.description_en.strip()

        return ""




class HistorySerializer(LocalizationSerializerMixin, serializers.ModelSerializer):
    description = serializers.SerializerMethodField()

    class Meta:
        model = History
        fields = ["id", "description", "image", "order"]
        read_only_fields = ["id"]

    def get_description(self, obj):
        language = self._get_language()
        field_name = f"description_{language}"
        return getattr(obj, field_name, obj.description_ru)


class StructureSerializer(LocalizationSerializerMixin, serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = Structure
        fields = [
            "id",
            "slug",
            "category",
            "logo",
            "name",
            "description",
            "address",
            "email",
            "phone",
            "order",
        ]
        read_only_fields = ["id"]
        lookup_field = "slug"

    def get_name(self, obj):
        return obj.get_name(language=self._get_language())

    def get_description(self, obj):
        language = self._get_language()
        # Получаем RichText content и возвращаем как есть (с HTML тегами)
        return obj.get_description(language=language)

    def get_address(self, obj):
        return obj.get_address(language=self.context.get("language")
)
    