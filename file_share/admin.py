from django.contrib import admin
from .models import User, Post, Comment

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'password']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'file_field']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content']