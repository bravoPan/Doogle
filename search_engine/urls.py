from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.index, name="index"),
    # path(r'^$', views.index, name="index"),
    path(r'<int:question_id>/', views.detail, name="detail"),
    path(r'<int:question_id>/results/', views.results, name="results"),
    path(r'<int:question_id>/vote', views.vote, name="vote"),
    path(r'<str:key_words>/', views.display, name="search_keywords")
]
