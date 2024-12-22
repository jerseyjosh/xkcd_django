from django.urls import path
from .views import comic_list, search_comics

urlpatterns = [
    path('', comic_list, name='comic_list'),
    path('search/', search_comics, name='search_comics'),
]
