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
    assert reverse("post_update", kwargs={"slug": post.slug}) in content


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


@pytest.mark.django_db
def test_post_detail_renders_rich_text_content(client):
    post = Post.objects.create(
        title="Artigo com formato",
        excerpt="Resumo com formato.",
        cover_image="https://example.com/rich.jpg",
        content=(
            "<p><strong>Texto forte</strong> com <em>itálico</em> ✅</p>"
            "<h2>Subtitulo</h2>"
            "<blockquote>Destaque importante</blockquote>"
        ),
        published=True,
    )

    response = client.get(reverse("post_detail", kwargs={"slug": post.slug}))
    content = response.content.decode()

    assert "<strong>Texto forte</strong>" in content
    assert "<em>itálico</em>" in content
    assert "<h2>Subtitulo</h2>" in content
    assert "<blockquote>Destaque importante</blockquote>" in content
    assert "✅" in content


@pytest.mark.django_db
def test_post_update_returns_success(client, post):
    response = client.get(reverse("post_update", kwargs={"slug": post.slug}))

    assert response.status_code == 200
    assert "Edit blog post" in response.content.decode()


@pytest.mark.django_db
def test_post_update_persists_changes(client, post):
    response = client.post(
        reverse("post_update", kwargs={"slug": post.slug}),
        data={
            "title": "Updated post title",
            "excerpt": "Updated excerpt.",
            "cover_image": "https://example.com/updated.jpg",
            "content": "<p>Updated content.</p>",
            "published": "on",
            "published_at": "2026-04-25T10:30",
        },
    )

    post.refresh_from_db()

    assert response.status_code == 302
    assert response.url == post.get_absolute_url()
    assert post.title == "Updated post title"
    assert post.excerpt == "Updated excerpt."
    assert post.cover_image == "https://example.com/updated.jpg"
    assert post.content == "<p>Updated content.</p>"
