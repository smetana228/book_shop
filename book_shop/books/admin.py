from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','book_author','cover','price','stock','av')
    list_filter = ('genre', 'pub_date','book_author')
    list_editable = ('price','stock','av')
    readonly_fields = ["cover"]
    def cover(self, obj):
        return mark_safe(f'<img src="{obj.book_cover.url}" style="max-height: 150px;">')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name','im','age','nation')
    list_filter=('century','nation')
    readonly_fields = ["im"]
    def im(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="max-height: 100px;">')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_filter=('revdate','book')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('userr','pfp')
    readonly_fields = ["pfp"]
    def pfp(self, obj):
        return mark_safe(f'<img src="{obj.profile_pic.url}" style="max-height: 100px;">')
admin.site.register(BookGenre)


