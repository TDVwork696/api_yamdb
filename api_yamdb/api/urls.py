from rest_framework import routers

from django.urls import include, path

from api.views import (APISignup, APIGetToken, CategoriesViewSet,
                       GenresViewSet, TitlesViewSet, UsersViewSet)

router_api_v1 = routers.DefaultRouter()
router_api_v1.register(r'categories', CategoriesViewSet, basename='categories')
router_api_v1.register(r'genres', GenresViewSet, basename='genres')
router_api_v1.register(r'titles', TitlesViewSet, basename='titles')
router_api_v1.register(r'users', UsersViewSet, basename='users')


urlpatterns_auth = [
    path('signup/', APISignup.as_view(), name='signup'),
    path('token/', APIGetToken.as_view(), name='get_token')
]

urlpatterns = [
    path('v1/auth/', include(urlpatterns_auth)),
    path('v1/', include(router_api_v1.urls)),
]
