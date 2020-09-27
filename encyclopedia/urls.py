from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.display_page, name="display"),
    path("search/", views.search, name="search"),
    path("random/", views.random_page, name="random"),
    path("newpage/", views.new_page, name="newpage"),
    path("wiki/<str:title>/edit/", views.edit, name="edit")
]
