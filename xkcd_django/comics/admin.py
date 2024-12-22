from django.contrib import admin
from .models import Comic

@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = ('comic_number', 'title', 'publish_date')
    search_fields = ('title', 'alt')
    list_filter = ('publish_date',)
