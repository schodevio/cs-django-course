from django.urls import path

from .views import (
    PostListView,
    UserPostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)

from . import views

urlpatterns = [
    path("", PostListView.as_view(), name="blog_home"),
    path("user/<str:username>/", UserPostListView.as_view(), name="blog_user_posts"),
    path("posts/new/", PostCreateView.as_view(), name="blog_new_post"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="blog_post"),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="blog_edit_post"),
    path("posts/<int:pk>/delete/",
         PostDeleteView.as_view(), name="blog_delete_post"),
    path("about/", views.about, name="blog_about"),
]
