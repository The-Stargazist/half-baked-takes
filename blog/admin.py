from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'published', 'created_at']
    list_filter = ['category', 'published']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
