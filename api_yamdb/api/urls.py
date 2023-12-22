from django.urls import include, path
from rest_framework import routers

from api.views import (APIAuth, CategoriesViewSet,
                       GenresViewSet, TitlesViewSet, UsersViewSet,
                       ReviewsViewSet, CommentsViewSet)

router_api_v1 = routers.DefaultRouter()
router_api_v1.register(r'categories', CategoriesViewSet, basename='categories')
router_api_v1.register(r'genres', GenresViewSet, basename='genres')
router_api_v1.register(r'titles', TitlesViewSet, basename='titles')
router_api_v1.register(r'users', UsersViewSet, basename='users')
router_api_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                       ReviewsViewSet, basename='reviews')
router_api_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments')
router_api_v1.register(r'auth', APIAuth, basename='auth')


urlpatterns = [
    path('v1/', include(router_api_v1.urls)),
]
