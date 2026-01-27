# views.py
from rest_framework import generics
from .models import Partner
from .serializers import PartnerSerializer


class LanguageContextMixin:
    """Миксин для добавления языка в context сериализатора"""
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context



class PartnerListView(generics.ListAPIView):
    """
    View для получения списка всех партнеров
    Поддерживает параметр lang для выбора языка (ru, en, kg)
    """
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["language"] = self.request.query_params.get("lang", "ru")
        return context

    

class PartnerDetailView(generics.RetrieveAPIView, LanguageContextMixin):
    """
    View для получения детальной информации о партнере
    Поддерживает параметр lang для выбора языка (ru, en, kg)
    """
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    lookup_field = 'id'
