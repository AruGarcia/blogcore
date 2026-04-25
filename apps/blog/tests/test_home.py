import pytest
from django.urls import reverse
from django.utils.html import escape

from apps.blog.views import ARTICLES, FEATURED_ARTICLE


@pytest.fixture
def home_response(client):
    return client.get(reverse("home"))


def test_home_page_returns_success(home_response):
    assert home_response.status_code == 200


def test_home_page_uses_expected_templates(home_response):
    template_names = [template.name for template in home_response.templates if template.name]

    assert "blog/home.html" in template_names
    assert "blog.html" in template_names


def test_home_page_renders_main_sections(home_response):
    content = home_response.content.decode()

    assert "bootstrap@5.3.8" in content
    assert "Blog" in content
    assert "All articles" in content
    assert "Manage bookings and payments easier" in content


def test_home_page_includes_featured_article_content(home_response):
    content = home_response.content.decode()

    assert FEATURED_ARTICLE["title"] in content
    assert FEATURED_ARTICLE["date"] in content
    assert escape(FEATURED_ARTICLE["image"]) in content


def test_home_page_exposes_articles_in_context(home_response):
    assert home_response.context["featured_article"] == FEATURED_ARTICLE
    assert home_response.context["articles"] == ARTICLES
    assert len(home_response.context["articles"]) == 6


def test_home_page_renders_all_article_cards(home_response):
    content = home_response.content.decode()

    for article in ARTICLES:
        assert article["title"] in content
        assert article["date"] in content
        assert escape(article["image"]) in content
