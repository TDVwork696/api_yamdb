from rest_framework import routers

from django.urls import include, path

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet

router_api_v1 = routers.DefaultRouter()
router_api_v1.register(r'categories', CategoriesViewSet, basename='categories')
router_api_v1.register(r'genres', GenresViewSet, basename='genres')
router_api_v1.register(r'titles', TitlesViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router_api_v1.urls)),
]
