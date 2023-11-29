#from rest_framework import filters
from django_filters import rest_framework as filters
#import django_filters
from reviews.models import Titles

class FilterSlug(filters.FilterSet):
    """
    Фильтр для поиска по полю slug
    """
    #slug = django_filters.OrderingFilter(fields=('created_at',))

    class Meta:
        model = Titles
        fields = ['genre__slug',]
    #def filter_queryset(self, request, queryset, view):
    #    slug = request.query_params.get('genre')
    #    return Genres.objects.filter(slug=slug)
