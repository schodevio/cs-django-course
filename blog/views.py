from django.shortcuts import render

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
# Create your views here.


def home(request):
    context = {
        "posts": posts
    }

    return render(request, "blog/home.html", context)


def about(request):
    context = {
        "title": "About"
    }

    return render(request, "blog/about.html", context)
