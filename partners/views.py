# views.py
from rest_framework import generics
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Partner, Projects
from .serializers import PartnerSerializer, ProjectsSerializer


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



class ProjectsViewSet(LanguageContextMixin, ReadOnlyModelViewSet):

    queryset = Projects.objects.all().order_by("-created_at")
    serializer_class = ProjectsSerializer

    @action(detail=False, methods=['get'])
    def banners(self, request):
        banners = self.get_queryset().filter(is_banner=True)
        serializer = self.get_serializer(banners, many=True)
        return Response(serializer.data)
