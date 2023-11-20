from rest_framework import routers

from django.urls import include, path

from .views import (CategoriesViewSet, GenresViewSet, TitlesViewSet,
                    ReviewsViewSet, CommentsViewSet)

router_api_v1 = routers.DefaultRouter()
router_api_v1.register(r'categories', CategoriesViewSet, basename='categories')
router_api_v1.register(r'genres', GenresViewSet, basename='genres')
router_api_v1.register(r'titles', TitlesViewSet, basename='titles')
router_api_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                       ReviewsViewSet, basename='reviews')
router_api_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_api_v1.urls)),
]
