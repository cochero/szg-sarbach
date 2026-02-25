from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'post_type', 'date', 'author', 'is_active']
    list_filter = ['post_type', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description']
