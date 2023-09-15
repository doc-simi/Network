
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.new_post, name="new_post"),
    path("posts", views.posts, name="posts"),
    path("like-post", views.likepost, name="like_post"),
    path("like-comment", views.likecomment, name="like_comment"),
    path("post-comment", views.postcomment, name="post_comment"),
    path("edit-post", views.editpost, name="edit_post"),
    path("user/<int:user_id>", views.user, name="user"),
    path("posts/<int:user_id>", views.user_posts, name="user_posts"),
    path("followers/<int:user_id>", views.followers, name="followers"),
    path("following/<int:user_id>", views.following, name="following"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("custom", views.my_followingPosts, name="my_followingPosts"),
    path("customposts", views.customposts, name="customposts"),



]





