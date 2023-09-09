from django.contrib import admin
from blog.models import Category, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Админ'''


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    '''Локация'''


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    '''Пост'''


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
