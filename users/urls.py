from django.urls import path
from . import views

urlpatterns = [
    path("new/", views.new, name="users-new"),
    path("", views.create, name="users-create"),
    path("profile/", views.profile, name="users-profile"),
]
