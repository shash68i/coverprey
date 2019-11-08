from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = ('created', 'publish', 'author')
    search_fields = ('title', 'body', 'book_name')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('publish',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'created')
    list_filter = ('created', 'updated')
    search_fields = ('body',)