from django.urls import path
from . import views

urlpatterns = [
    path("new/", views.new, name="users_new"),
    path("", views.create, name="users_create"),
    path("profile/", views.profile, name="users_profile"),
    path("profile/update/", views.update_profile, name="users_profile_update"),
]
