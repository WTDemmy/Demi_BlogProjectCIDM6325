from django.contrib import admin
from .models import Post 

# Register your models here.

from .models import BlogPost, Comment

admin.site.register(BlogPost)
admin.site.register(Comment) 


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")
    list_filter = ("created_at", "author")
    search_fields = ("title", "content")
