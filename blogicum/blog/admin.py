from django.contrib import admin
from .models import Category, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


class BlogAdmin(admin.ModelAdmin):
    '''Модель для вывода постов'''
    list_display = (
        'title',
        'author',
        'pub_date',
        'category',
        'is_published',
        'text',
    )
