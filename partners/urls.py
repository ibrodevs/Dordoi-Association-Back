# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'partners'
router = DefaultRouter()
router.register(r"projects", views.ProjectsViewSet, basename="news")

urlpatterns = [
    path('partners/', views.PartnerListView.as_view(), name='partner-list'),
    path('partners/<int:id>/', views.PartnerDetailView.as_view(), name='partner-detail'),
    path('partners/', include(router.urls))
]