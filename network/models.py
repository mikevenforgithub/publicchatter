from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweet")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "user": self.user.username,
            "id": self.id,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "likes": self.likes
        }

class Comment(models.Model):
    body = models.TextField()
    tweetid = models.ForeignKey(Tweet, blank=True, default=1, related_name="fromuser", on_delete=models.CASCADE)
    commentby = models.ForeignKey( User, blank=True, default=1, related_name="fromuser", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
       'body': self.body,
       'tweetid': self.tweetid
      }

class Following(models.Model):
    user = models.ForeignKey(User, blank=True, default=1, related_name="followedby", on_delete=models.CASCADE)
    follows = models.ForeignKey(User, blank=True, default=1, related_name="follows", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} follows {self.follows.username}"


class Like(models.Model):
    tweet = models.ForeignKey(Tweet, blank=True, default=1, related_name="tweetliked", on_delete=models.CASCADE)
    likedby = models.ForeignKey(User, blank=True, default=1, related_name="likedby", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tweet.id} liked by {self.likedby}"

