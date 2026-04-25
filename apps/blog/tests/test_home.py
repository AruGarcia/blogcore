import pytest
from django.utils import timezone
from django.urls import reverse
from django.utils.html import escape

from apps.blog.models import Post


@pytest.fixture
def featured_post(db):
    return Post.objects.create(
        title="Primeira publicacao pelo admin",
        excerpt="Resumo da publicacao em destaque.",
        cover_image="https://example.com/featured.jpg",
        content="Conteudo completo da publicacao.",
        is_featured=True,
        published=True,
    )


@pytest.fixture
def posts(db):
    return [
        Post.objects.create(
            title="Guia de pilates para iniciantes",
            excerpt="Um guia introdutorio para sua audiencia.",
            cover_image="https://example.com/pilates.jpg",
            content="Texto do guia de pilates.",
            published=True,
            published_at=timezone.now() - timezone.timedelta(days=2),
        ),
        Post.objects.create(
            title="Como montar sua agenda editorial",
            excerpt="Planejamento basico para publicar com consistencia.",
            cover_image="https://example.com/editorial.jpg",
            content="Texto sobre agenda editorial.",
            published=True,
            published_at=timezone.now() - timezone.timedelta(days=1),
        ),
    ]


@pytest.fixture
def home_response(client, featured_post, posts):
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


def test_home_page_includes_featured_article_content(home_response, featured_post):
    content = home_response.content.decode()

    assert featured_post.title in content
    assert escape(featured_post.cover_image) in content


def test_home_page_exposes_articles_in_context(home_response, featured_post, posts):
    assert home_response.context["featured_article"] == featured_post
    assert {post.pk for post in home_response.context["articles"]} == {
        featured_post.pk,
        *(post.pk for post in posts),
    }
    assert len(home_response.context["articles"]) == 3


def test_home_page_renders_all_article_cards(home_response, featured_post, posts):
    content = home_response.content.decode()

    for article in [featured_post, *posts]:
        assert article.title in content
        assert escape(article.cover_image) in content


def test_home_page_uses_shared_header_and_footer(home_response):
    content = home_response.content.decode()

    assert 'class="navbar navbar-expand-lg sticky-top site-nav"' in content
    assert 'id="resources"' in content
    assert "Privacy Policy" in content


def test_home_page_orders_articles_by_latest_publication(home_response, featured_post, posts):
    ordered_titles = [post.title for post in home_response.context["articles"]]

    assert ordered_titles == [
        featured_post.title,
        posts[1].title,
        posts[0].title,
    ]


@pytest.mark.django_db
def test_home_page_hides_unpublished_posts(client):
    Post.objects.create(
        title="Rascunho privado",
        excerpt="Nao deve aparecer na home.",
        cover_image="https://example.com/draft.jpg",
        content="Rascunho",
        published=False,
    )

    response = client.get(reverse("home"))

    assert response.status_code == 200
    assert "Rascunho privado" not in response.content.decode()
