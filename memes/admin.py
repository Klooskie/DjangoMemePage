from django.contrib import admin

from .models import Meme, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    readonly_fields = ('author', 'comment_text', 'pub_date')
    extra = 0


class MemeAdmin(admin.ModelAdmin):
    readonly_fields = ('author',
                       'title',
                       'image',
                       'height_field',
                       'width_field',
                       'pub_date',
                       'get_number_of_likes',
                       'get_number_of_dislikes')
    list_display = ('title', 'author', 'pub_date')
    inlines = [CommentInline]


admin.site.register(Meme, MemeAdmin)
