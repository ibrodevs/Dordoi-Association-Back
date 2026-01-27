from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import FactCard, Leader, History, Structure
from .serializers import (
    FactCardSerializer,
    LeaderSerializer,
    HistorySerializer,
    StructureSerializer,
)
from rest_framework import generics


class LeaderListView(generics.ListAPIView):
    """
    View для получения списка всех лидеров
    Поддерживает параметр lang для выбора языка (ru, en, kg)
    """

    queryset = Leader.objects.all()
    serializer_class = LeaderSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context


class LeaderDetailView(generics.RetrieveAPIView):
    """
    View для получения детальной информации о лидере
    Поддерживает параметр lang для выбора языка (ru, en, kg)
    """

    queryset = Leader.objects.all()
    serializer_class = LeaderSerializer
    lookup_field = "id"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context


class LocalizationMixin:
    """Миксин для передачи языка в контекст сериализатора"""

    def get_serializer_context(self):
        context = super().get_serializer_context()
        language = (
            self.request.GET.get("lang")
            or getattr(self.request, "LANGUAGE_CODE", None)
            or "ru"
        )
        context.update({"language": language})
        return context


class BannerFact(LocalizationMixin, generics.ListAPIView):
    """
    View для получения списка факт-карт, отмеченных как баннеры
    Поддерживает параметр lang для выбора языка (ru, en, kg)
    """

    queryset = FactCard.objects.filter(is_banner=True).order_by("id")
    serializer_class = FactCardSerializer


class FactCardViewSet(LocalizationMixin, ReadOnlyModelViewSet):
    """
    ViewSet для получения факт-карт с деталями.

    Query Parameters:
    - lang: ru, en, kg (язык ответа)
    - ordering: id, title_ru, title_en, title_kg
    - search: поиск по названию и описанию
    """

    queryset = FactCard.objects.all().order_by("id")
    serializer_class = FactCardSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        "title_en",
        "title_ru",
        "title_kg",
        "description_en",
        "description_ru",
        "description_kg",
        "detail_en",
        "detail_ru",
        "detail_kg",
    ]
    ordering_fields = ["id", "title_ru", "title_en", "title_kg"]


class HistoryViewSet(LocalizationMixin, ReadOnlyModelViewSet):
    """
    Read-only viewset для истории — появится в корне роутера /api/about-us/
    Поддерживает параметр ?lang=ru|en|kg
    """

    queryset = History.objects.all().order_by("order")
    serializer_class = HistorySerializer
    ordering_fields = ["order"]


class StructureViewSet(LocalizationMixin, ReadOnlyModelViewSet):
    """
    Read-only viewset для структурных подразделений
    Поддерживает параметр ?lang=ru|en|kg
    Поиск по slug: /api/about-us/structure/dordoi-trade/
    """

    queryset = Structure.objects.all().order_by("order").filter(is_active=False)
    serializer_class = StructureSerializer
    lookup_field = "slug"
   

