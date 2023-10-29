from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="root"),
    path("tag/", views.tag, name="tag"),
    path("quote/", views.quote, name="quote"),
    path("author/", views.author, name="author"),
    path("about/<author_id>", views.about, name="about"),
    path("<int:page>", views.main, name="root_paginate"),
]
