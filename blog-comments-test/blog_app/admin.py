from django.contrib import admin
from .models import Blog, Comment
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','num_comments')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('content','path_id','num_replies','level')

admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment,CommentAdmin)
