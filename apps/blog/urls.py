from django.urls import path

from .views import home, post_create, post_detail, post_update

urlpatterns = [
    path("", home, name="home"),
    path("artigos/novo/", post_create, name="post_create"),
    path("artigos/<slug:slug>/editar/", post_update, name="post_update"),
    path("artigos/<slug:slug>/", post_detail, name="post_detail"),
]
