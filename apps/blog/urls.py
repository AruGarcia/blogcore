from django.urls import path

from .views import home, post_detail

urlpatterns = [
    path("", home, name="home"),
    path("artigos/<slug:slug>/", post_detail, name="post_detail"),
]
