from django.urls import resolve, reverse

from apps.blog.views import home, post_detail


def test_home_url_resolves_to_home_view():
    assert reverse("home") == "/"
    assert resolve("/").func == home


def test_post_detail_url_resolves_to_detail_view():
    path = reverse("post_detail", kwargs={"slug": "meu-artigo"})

    assert path == "/artigos/meu-artigo/"
    assert resolve(path).func == post_detail
