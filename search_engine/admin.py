from django.contrib import admin
from search_engine.models import PageInfo, WordList, Href

# Register your models here.

admin.site.register(PageInfo)
admin.site.register(WordList)
admin.site.register(Href)
