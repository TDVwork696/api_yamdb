from rest_framework import viewsets, mixins


class CreateListDeleteViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """Класс для создания и отображения списка обьектов,
    а так же удаления отдельных обьектов"""
    pass
