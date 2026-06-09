from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from . import views

urlpatterns = [
    path("", PostListView.as_view(), name="blog-home"),
    path("posts/new/", PostCreateView.as_view(), name="blog-new-post"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="blog-post"),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="blog-edit-post"),
    path("posts/<int:pk>/delete/",
         PostDeleteView.as_view(), name="blog-delete-post"),
    path("about/", views.about, name="blog-about"),
]
