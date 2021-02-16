import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Tweet, Following, Like
from .forms import *


def index(request):

    # Authenticated users view their inbox
    if request.user.is_authenticated:
        tweets = list(reversed(Tweet.objects.all()))
        likes = Like.objects.all()
        user = request.user
        p = Paginator(tweets, 10)
        page_num = request.GET.get('page', 1)
        try:
           page = p.page(page_num)
        except EmptyPage:
           page = p.page(1)
        
        liked = Like.objects.filter(likedby=user.id)
        ls = []
        for i in liked: 
            ls.append(i.tweet) #all tweets liked by the user 
        lsid = []
        for i in ls: 
            lsid.append(i.id)# the id of all tweets liked by the user

        return render (request, "network/index.html",{
        "tweets": page,
        "likes" : likes,  
        "user": user,
        "liked": lsid    })
    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))




@csrf_exempt
@login_required
def compose(request):

    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    # Get contents of tweet
    body = data.get("body", "")

    # Create one email for each recipient, plus sender
    users = set()
    users.add(request.user)
    for user in users:
        tweet = Tweet(
            user=user,
            body=body,
        )
        tweet.save()
        return JsonResponse({"message": "Tweet saved successfully."}, status=201)


@login_required
def tweetbox(request, tweetbox):

    # Filter emails returned based on mailbox
    if tweetbox == "alltweets":
        tweets = Tweet.objects.all()

    elif tweetbox == "following":
        tweets = Tweet.objects.filter(
            user=request.user
        )
    else:
        return JsonResponse({"error": "Invalid mailbox."}, status=400)

    # Return emails in reverse chronologial order
    tweets = tweets.order_by("-timestamp").all()
    return JsonResponse([tweet.serialize() for tweet in tweets], safe=False)


@csrf_exempt
@login_required
def tweet(request, tweet_id):

    # Query for requested email
    try:
        tweet = Tweet.objects.get(id=tweet_id)
    except Tweet.DoesNotExist:
        return JsonResponse({"error": "Tweet not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(tweet.serialize())

    # Update whether email is read or should be archived
    elif request.method == "PUT":
        data = json.loads(request.body)
        tweet.save()
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "network/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def profile(request):
    user = request.user
    tweets = reversed(Tweet.objects.filter(user=user))
    followed = Following.objects.filter(follows=user)
    following = Following.objects.filter(user=user)
    followed = int(len(followed))
    following = int(len(following))
    return render(request, "network/profile.html", {
        "user" : user,
        "posts": tweets,
        "followed" : followed,
        "following" : following
        
    })


def userprofile(request, username):
    user = request.user
    username = User.objects.filter(username=username).first()
    usr = username
    tweets = reversed(Tweet.objects.filter(user=usr))
    followed = Following.objects.filter(follows=usr)
    following = Following.objects.filter(user=usr)
    followed = int(len(followed))
    following = int(len(following))

    flw = Following.objects.filter(user=request.user)
    ls =[]
    for i in flw:
        ls.append(i.follows)

    liked = Like.objects.filter(likedby=user.id)
    l = []
    for i in liked: 
        l.append(i.tweet) #all tweets liked by the user 
    lsid = []
    for i in l: 
        lsid.append(i.id)# the id of all tweets liked by the user
    return render(request, "network/profile.html", {
        "user": user,
        "usr" : username,
        "posts": tweets,
        "followed" : followed,
        "following" : following,
        "ls" : ls,
        "liked": lsid 
        
    })


def following(request):
    user = request.user
    following = Following.objects.filter(user=user).values('follows_id')
    tweets = list(Tweet.objects.filter(user__in=following).order_by('-timestamp'))
    p = Paginator(tweets, 10)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    liked = Like.objects.filter(likedby=user.id)
    ls = []
    for i in liked: 
        ls.append(i.tweet) #all tweets liked by the user 
    lsid = []
    for i in ls: 
        lsid.append(i.id)# the id of all tweets liked by the user

    return render (request, "network/following.html",{
            "tweets": page,
            "liked": lsid
            })


def addtofollowing(request, usr):
    if request.method == "POST":
        form = AddFollowed(request.POST)
        if form.is_valid():
            user1 = request.user.username
            usercur = User.objects.filter(username=user1).first()
            usertofollow = User.objects.filter(username=usr).first()
            follow = Following.objects.filter(user=usercur).all()
            if usertofollow.username not in follow:
                newfollow = Following.objects.create(user=usercur,follows=usertofollow)
                user = request.user
                following = Following.objects.filter(user=user).values('follows_id')
                tweets = Tweet.objects.filter(user__in=following).order_by('-timestamp')
                return render (request, "network/following.html",{
                        "tweets": tweets,
                        })
            
def removefollowing(request, usr):
    if request.method == "POST":
            form = AddFollowed(request.POST)
            if form.is_valid():
                user1 = request.user.username
                usercur = User.objects.filter(username=user1).first()
                usertofollow = User.objects.filter(username=usr).first()
                follow = Following.objects.filter(user=usercur).all()
                notfollow = Following.objects.filter(user=usercur,follows=usertofollow).delete()
                user = request.user
                following = Following.objects.filter(user=user).values('follows_id')
                tweets = Tweet.objects.filter(user__in=following).order_by('-timestamp')
                return render (request, "network/following.html",{
                        "tweets": tweets,
                        })
    
            
                    

@csrf_exempt
def edit(request, post_id):
    post = Tweet.objects.get(id=post_id)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("body") is not None:
            post.body = data["body"]
        post.save()
        return HttpResponse(status=204)

@csrf_exempt
def like(request, post_id):
    post = Tweet.objects.get(id=post_id)

    if request.method == "GET":
        return JsonResponse(post.serialize())

    if request.method == "PUT":
        data = json.loads(request.body)
        print(data.get("like"))
        if data.get("like"):
            Like.objects.create(likedby=request.user, tweet=post)
            post.likes = Like.objects.filter(tweet=post).count()
        else: # unlike
            Like.objects.filter(likedby=request.user, tweet=post).delete()
            post.likes = Like.objects.filter(tweet=post).count()
        post.save()
        

