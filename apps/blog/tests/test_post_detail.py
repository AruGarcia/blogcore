import pytest
from django.urls import reverse

from apps.blog.models import Post


@pytest.fixture
def post(db):
    return Post.objects.create(
        title="Como estruturar um artigo de blog",
        excerpt="Um resumo editorial para a página de detalhe.",
        cover_image="https://example.com/detail.jpg",
        content="Primeiro paragrafo.\n\nSegundo paragrafo.",
        published=True,
    )


@pytest.mark.django_db
def test_post_detail_returns_success(client, post):
    response = client.get(reverse("post_detail", kwargs={"slug": post.slug}))

    assert response.status_code == 200


@pytest.mark.django_db
def test_post_detail_uses_expected_template(client, post):
    response = client.get(reverse("post_detail", kwargs={"slug": post.slug}))
    template_names = [template.name for template in response.templates if template.name]

    assert "blog/post_detail.html" in template_names
    assert "blog.html" in template_names


@pytest.mark.django_db
def test_post_detail_renders_post_content(client, post):
    response = client.get(reverse("post_detail", kwargs={"slug": post.slug}))
    content = response.content.decode()

    assert post.title in content
    assert post.excerpt in content
    assert "Primeiro paragrafo." in content
    assert "Segundo paragrafo." in content
    assert "Manage bookings and payments easier" in content


@pytest.mark.django_db
def test_post_detail_hides_unpublished_posts(client):
    post = Post.objects.create(
        title="Artigo privado",
        excerpt="Nao pode abrir.",
        cover_image="https://example.com/private.jpg",
        content="Rascunho privado.",
        published=False,
    )

    response = client.get(reverse("post_detail", kwargs={"slug": post.slug}))

    assert response.status_code == 404


@pytest.mark.django_db
def test_home_links_to_post_detail(client):
    post = Post.objects.create(
        title="Artigo navegavel",
        excerpt="Resumo do artigo navegavel.",
        cover_image="https://example.com/link.jpg",
        content="Conteudo publico.",
        published=True,
    )

    response = client.get(reverse("home"))

    assert post.get_absolute_url() in response.content.decode()


@pytest.mark.django_db
def test_post_detail_uses_shared_header_and_footer(client, post):
    response = client.get(reverse("post_detail", kwargs={"slug": post.slug}))
    content = response.content.decode()

    assert 'class="navbar navbar-expand-lg sticky-top site-nav"' in content
    assert 'id="resources"' in content
    assert "Terms of Service" in content
