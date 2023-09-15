import json
from django.contrib.auth import authenticate, login, logout
from django.core import paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator

from .models import User, Post, Comment, PostLike, CommentLike, Follow




def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
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
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def new_post(request):

    if request.method != "POST":
        return JsonResponse({"message": "POST request required."}, status=400)

    data = json.loads(request.body)
    if data.get("content") == "":
        return JsonResponse({
            "message": "Post content is empty!"
        }, status=400)
    
    new_post = Post(user=request.user, content=data.get("content"))
    new_post.save()

    return JsonResponse({"message": "Post uploaded successfully."}, status=201)


def posts(request):
    posts = Post.objects.all()
    posts_count = posts.count()
    posts = posts.order_by("-timestamp")
    start = int(request.GET.get("start"))
    end = int(request.GET.get("end"))
    posts = posts[start:end]

    return JsonResponse({"posts_count": posts_count,
    "posts":[post.serialize() for post in posts]}, safe=False)

@login_required
def user_posts(request, user_id):
    posts = Post.objects.filter(user_id=user_id)
    posts_count = posts.count()
    posts = posts.order_by("-timestamp")
    start = int(request.GET.get("start"))
    end = int(request.GET.get("end"))
    posts = posts[start:end]
    

    return JsonResponse({"posts_count": posts_count,
    "posts":[post.serialize() for post in posts]}, safe=False)

@csrf_exempt
def likepost(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        post_id = int(data.get("post"))
        post = Post.objects.get(pk=post_id)
        user = request.user.id

        if not user:
            return JsonResponse({"message": "Log in to perform action", "status":True}, status=400)

        list_of_likers = [a.user.id for a in post.post_likes.all()]
        if user in list_of_likers:
            PostLike.objects.filter(user_id=user).delete()
            post.likes -= 1
        else:
            new_like = PostLike(post=post, user_id=user)
            new_like.save()

            post.likes += 1
        post.save()

        new_no_likes = post.likes
        list_of_likers = [a.user.id for a in post.post_likes.all()]


        liked = True if user in list_of_likers else False

        return JsonResponse({
            "no_likes": new_no_likes,
            "liked": liked
        }, status=201)

@csrf_exempt
def likecomment(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        comment_id = int(data.get("comment"))
        comment = Comment.objects.get(pk=comment_id)
        user = request.user.id

        if not user:
            return JsonResponse({"message": "Log in to perform action", "status":True}, status=400)

        list_of_likers = [a.user.id for a in comment.comment_likes.all()]
        if user in list_of_likers:
            comment.likes -= 1
            CommentLike.objects.filter(user_id=user).delete()
        else:
            comment.likes += 1
            new_like = CommentLike(comment=comment, user_id=user)
            new_like.save()

        comment.save()

        new_no_likes = comment.likes
        list_of_likers = [a.user.id for a in comment.comment_likes.all()]


        liked = True if user in list_of_likers else False

        return JsonResponse({
            "no_likes": new_no_likes,
            "liked": liked
        }, status=201)



@csrf_exempt
def postcomment(request):
    if request.method != 'POST':
        return JsonResponse({"message": "invalid request", "status": True}, status=400)

    data = json.loads(request.body)
    user = request.user.id
    comment = data.get("comment")
    post_id = int(data.get("post"))
    
    if not user:
            return JsonResponse({"message": "Log in to perform action", "status": True}, status=400)

    if not comment:
        return JsonResponse({"message": "comment can't be empty!", "status": True}, status=400) 

    post = Post.objects.get(pk=post_id)

    new_comment = Comment(post=post, user_id=user, comment=comment)
    new_comment.save()

    post.comments_count += 1
    post.save()

    comments = post.comments.all()

    return JsonResponse({"comments": [x.serialize() for x in comments],
    "status": False}, status=201)

@csrf_exempt
@login_required
def editpost(request):
    if request.method != "POST":
        return JsonResponse({"message": "POST request required."}, status=400)

    data = json.loads(request.body)
    if data.get("content") == "":
        return JsonResponse({
            "message": "Post content is empty!",
            "status": True
        }, status=400)
    
    if request.user.id != int(data.get("user_id")):
        return JsonResponse({
            "message": "Access not granted",
            "status": True
        })
    
    content = data.get("content")
    post_id = int(data.get("id"))

    
    post = Post.objects.get(pk=post_id)
    post.content = content
    post.save()

    new_post = post.content

    return JsonResponse({"message": "Edited successfully.",
    "post": new_post}, status=201)


def user(request, user_id):
    f = User.objects.get(pk=user_id)
    is_following = False

    if request.user.id:

        if user_id != request.user.id:
            try:
                check_following = Follow.objects.get(follower=request.user.id, following=user_id)
            
            except Follow.DoesNotExist:
                check_following = None

            is_following = True if check_following else False
        


    return render(request, "network/user.html", {
        "user_profile": f,
        "date": f.date_joined.strftime("%B %Y"),
        "following": is_following
    })

def followers(request, user_id):
    followers = []
    try:
        followers = Follow.objects.filter(following_id=user_id)
        followers = [x.follower for x in followers]
    except Follow.DoesNotExist:
        pass
    return render(request, "network/followpage.html", {
        "lists": followers,
        "title": "Followers"
    })

def following(request, user_id):
    following = []
    try:
        following = Follow.objects.filter(follower_id=user_id)
        following = [x.following for x in following]
    except Follow.DoesNotExist:
        pass


    return render(request, "network/followpage.html", {
        "lists": following,
        "title": "Following"
    })

@csrf_exempt
def follow(request, user_id):
    
    user_follower = User.objects.get(pk=request.user.id)
    user_following = User.objects.get(pk=user_id)
    

    try:
        following = Follow.objects.get(follower_id=request.user.id, following_id=user_id)
        following.delete()
        user_following.followers -= 1
        user_follower.following -= 1

        is_following = False

    except Follow.DoesNotExist:
        try:
            new_follow = Follow(follower_id=request.user.id, following_id=user_id)
            new_follow.save()
        except IntegrityError:
            pass
        user_following.followers += 1
        user_follower.following += 1
        
        is_following = True

    user_follower.save()
    user_following.save()

    return JsonResponse({"is_following": is_following,
    "followers": user_following.followers,
    "following": user_following.following
    }, status=201)

@login_required
def my_followingPosts(request):
    
    return render(request, "network/customposts.html")

def customposts(request):
    following = Follow.objects.filter(follower=request.user)
    following = [x.following for x in following]
    posts = Post.objects.filter(user__in=following)
    posts_count = posts.count()
    posts = posts.order_by("-timestamp")
    start = int(request.GET.get("start"))
    end = int(request.GET.get("end"))
    posts = posts[start:end]

    return JsonResponse({"posts": [post.serialize() for post in posts], "posts_count":posts_count, "empty":False}, status=201)