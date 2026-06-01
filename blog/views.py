from django.shortcuts import render
from .models import Post

posts = [
    {
        "author": "Szymek",
        "title": "Blog Post 1",
        "content": "Lorem ipsum",
        "created_at": "August 27, 2018"
    },
    {
        "author": "Jane",
        "title": "Blog Post 2",
        "content": "Dolor sit",
        "created_at": "August 28, 2018"
    }
]


def home(request):
    posts = Post.objects.all()

    return render(request, "blog/home.html", {"posts": posts})


def about(request):
    return render(request, "blog/about.html", {"title": "About"})
