from django.contrib import admin

from .models import Categories, Genres, Title
from user.models import CustomUser

admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Title)
admin.site.register(CustomUser)
