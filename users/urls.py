from django.urls import path
from . import views

urlpatterns = [
    path("", views.create, name="users-create"),
    path("new/", views.new, name="users-new"),
]
