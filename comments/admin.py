from django.contrib import admin

from comments.models import Post, Comment, Rate

admin.site.register(Post)
admin.site.register(Rate)
admin.site.register(Comment)
