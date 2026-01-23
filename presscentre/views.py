from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .models import Category, News, Publication
from .serializers import (
    PublicationSerializer,
    CategorySerializer,
    NewsSerializer,
)


class LocalizationMixin:

    def get_serializer_context(self):
        context = super().get_serializer_context()
        language = (
            self.request.GET.get("lang")
            or getattr(self.request, "LANGUAGE_CODE", None)
            or "ru"
        )
        context.update({"language": language})
        return context


class PublicationViewSet(LocalizationMixin, ReadOnlyModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    


class CategoryViewSet(LocalizationMixin, ReadOnlyModelViewSet):

    queryset = Category.objects.all().order_by("title_ru")
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        "title_en",
        "title_ru",
        "title_kg",
    ]
    ordering_fields = ["title_ru"]


class NewsViewSet(LocalizationMixin, ReadOnlyModelViewSet):

    queryset = News.objects.all().order_by("-created_at")
    serializer_class = NewsSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = [
        "title_en",
        "title_ru",
        "title_kg",
        "short_description_en",
        "short_description_ru",
        "short_description_kg",
        "description_en",
        "description_ru",
        "description_kg",
    ]
    ordering_fields = ["created_at", "published_at", "title_ru"]
    filterset_fields = ["category", "is_banner", "is_recommended"]

    @action(detail=False, methods=['get'])
    def banners(self, request):
        banners = self.get_queryset().filter(is_banner=True)
        serializer = self.get_serializer(banners, many=True)
        return Response(serializer.data)
