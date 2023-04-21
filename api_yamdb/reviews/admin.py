from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'text', 'author', 'pub_date')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'author', 'score', 'pub_date')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
