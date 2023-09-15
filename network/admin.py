from django.contrib import admin

from .models import User, Comment, Post, PostLike, CommentLike, Follow

# Register your models here.

admin.site.register(User),
admin.site.register(Comment),
admin.site.register(Post),
admin.site.register(PostLike),
admin.site.register(CommentLike),
admin.site.register(Follow),
