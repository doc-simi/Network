from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    date_joined = models.DateTimeField(auto_now_add=True)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)


class Post(models.Model):
    content = models.CharField(max_length=150)
    user = models.ForeignKey("User", on_delete=CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "body": self.content,
            "timestamp": self.timestamp.strftime("%I:%M %p. %d %b %y"),
            "likes": self.likes,
            "comments": self.comments_count,
            "user": self.user.username,
            "user_id": self.user.id,
            "allcomments": [x.serialize() for x in self.comments.all()],
            "liked_by": [x.user.id for x in self.post_likes.all()] 
        }
        
class Comment(models.Model):
    post = models.ForeignKey("Post", on_delete=CASCADE, related_name="comments")
    user = models.ForeignKey("User", on_delete=CASCADE)
    comment = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)


    def serialize(self):
        return {
            "id": self.id,
            "comment": self.comment,
            "timestamp": self.timestamp.strftime("%I:%M %p. %d %b %y"),
            "likes": self.likes,
            "user": self.user.username,
            "user_id": self.user.id,
            "comments_count": self.post.comments_count,
            "liked_by": [x.user.id for x in self.comment_likes.all()] 
        }

class Follow(models.Model):
    follower = models.ForeignKey("User", on_delete=CASCADE, related_name="my_following")
    following = models.ForeignKey("User", on_delete=CASCADE, related_name="my_followers")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name="unique_follows")
        ]
    
    def __str__(self):
        return f"{self.follower} follows {self.following}"


class PostLike(models.Model):
    post = models.ForeignKey("Post", on_delete=CASCADE, related_name="post_likes")
    user = models.ForeignKey("User", on_delete=CASCADE)

class CommentLike(models.Model):
    comment = models.ForeignKey("Comment", on_delete=CASCADE, related_name="comment_likes")
    user = models.ForeignKey("User", on_delete=CASCADE)