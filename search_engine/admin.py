from django.contrib import admin
from search_engine.models import Questions, Choice, WordList, WordLocation, UrlList

# Register your models here.

admin.site.register(Questions)
admin.site.register(Choice)
admin.site.register(WordList)
admin.site.register(UrlList)
admin.site.register(WordLocation)
