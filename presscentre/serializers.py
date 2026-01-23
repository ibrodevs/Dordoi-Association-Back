from rest_framework import serializers
from .models import Category, News, Publication, NewsPhoto
from Gallery.serializers import GallerySerializer


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


class PublicationSerializer(LocalizationSerializerMixin, serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Publication
        fields = [
            "id",
            "title",
            "link",
            'description',
            'photo',
        ]

    def get_description(self, obj):
        return obj.get_description(language=self._get_language())
    
    def get_title(self, obj):
        return obj.get_title(language=self._get_language())


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


class NewsPhotoSerializer(LocalizationSerializerMixin, serializers.ModelSerializer):
    alt_text = serializers.SerializerMethodField()

    class Meta:
        model = NewsPhoto
        fields = ['id', 'image', 'alt_text', 'order']

    def get_alt_text(self, obj):
        language = self._get_language()
        return obj.get_alt_text(language=language)


class NewsSerializer(LocalizationSerializerMixin, serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True)
    photos = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            "id",
            "title",
            "short_description",
            "description",
            "category",
            "is_banner",
            "is_recommended",
            "created_at",
            "updated_at",
            "published_at",
            "image",
            "photos",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_title(self, obj):
        return obj.get_title(language=self._get_language())

    def get_short_description(self, obj):
        return obj.get_short_description(language=self._get_language())

    def get_description(self, obj):
        return obj.get_description(language=self._get_language())

    def get_photos(self, obj):
        photos = obj.photos.all()
        return NewsPhotoSerializer(photos, many=True, context=self.context).data
