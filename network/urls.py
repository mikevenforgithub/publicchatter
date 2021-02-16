
from django.urls import path

from . import views

urlpatterns = [
    path("home", views.index, name="index"),
    path("following", views.following, name="following"),
    path("following/<str:usr>", views.addtofollowing, name="addtofollowing"),
    path("notfollowing/<str:usr>", views.removefollowing, name="removefollowing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("home/<str:username>", views.userprofile, name="userprofile"),
        # API Routes
    path("tweets", views.compose, name="compose"),
    path("tweets/<int:tweet_id>", views.tweet, name="tweet"),
    path("tweets/<str:tweetbox>", views.tweetbox, name="tweetbox"),
    path("edit/<int:post_id>", views.edit, name="edit"), 
    path("like/<str:post_id>", views.like, name="like")
]


