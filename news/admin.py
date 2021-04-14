from django.contrib import admin
from .models import News, NewsImage, NewsTag

admin.site.register(News)
admin.site.register(NewsImage)
admin.site.register(NewsTag)
