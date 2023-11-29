from rest_framework import filters

class FilterSlug(filters.SearchFilter):
    """
    Фильтр для поиска по полю slug
    """

    def get_search_fields(self, view, request):
        if request.query_params.get('genre__slug'):
            return ['slug']
        return super().get_search_fields(view, request)
