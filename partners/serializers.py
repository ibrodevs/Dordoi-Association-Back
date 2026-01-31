# serializers.py
from rest_framework import serializers
from .models import Partner, Category, Projects


class LocalizationSerializerMixin:

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


class PartnerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Partner
        fields = [
            'id',
            'logo',
            'name',
            'description',
            'coord1',
            'coord2',
        ]

    def get_name(self, obj):
        return obj.get_name(self.context.get("language", "ru"))

    def get_description(self, obj):
        return obj.get_description(self.context.get("language", "ru"))


class CategorySerializer(LocalizationSerializerMixin, serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "title",
        ]

    def get_title(self, obj):
        return obj.get_title(language=self._get_language())



class ProjectsSerializer(LocalizationSerializerMixin, serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Projects
        fields = [
            "id",
            "title",
            "short_description",
            "description",
            "category",
            "created_at",
            "updated_at",
            "published_at",
            "image",
            "image",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_title(self, obj):
        return obj.get_title(language=self._get_language())

    def get_short_description(self, obj):
        return obj.get_short_description(language=self._get_language())

    def get_description(self, obj):
        return obj.get_description(language=self._get_language())

