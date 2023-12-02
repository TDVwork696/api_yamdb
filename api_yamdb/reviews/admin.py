from django.contrib import admin

from user.models import CustomUser

from .models import Categories, Genres, Title

admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Title)
admin.site.register(CustomUser)
