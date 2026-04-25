import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from apps.blog.models import Post


@pytest.mark.django_db
def test_post_string_representation():
    post = Post.objects.create(
        title="Meu artigo",
        content="Conteudo do artigo.",
        published=True,
    )

    assert str(post) == "Meu artigo"


@pytest.mark.django_db
def test_post_generates_slug_from_title():
    post = Post.objects.create(
        title="Como Organizar Sua Agenda",
        content="Conteudo do artigo.",
        published=True,
    )

    assert post.slug == "como-organizar-sua-agenda"


@pytest.mark.django_db
def test_post_preserves_existing_slug():
    post = Post.objects.create(
        title="Titulo original",
        slug="slug-customizado",
        content="Conteudo do artigo.",
        published=True,
    )

    assert post.slug == "slug-customizado"


@pytest.mark.django_db
def test_post_absolute_url():
    post = Post.objects.create(
        title="Artigo com url",
        slug="artigo-com-url",
        content="Conteudo do artigo.",
        published=True,
    )

    assert post.get_absolute_url() == "/artigos/artigo-com-url/"


@pytest.mark.django_db
def test_post_fallback_cover_image_uses_local_file():
    post = Post.objects.create(
        title="Best Pricing Strategies for Pilates Studios in 2026",
        slug="best-pricing-strategies-for-pilates-studios-in-2026",
        content="Conteudo do artigo.",
        published=True,
    )

    assert (
        post.fallback_cover_image
        == (
            f"{settings.STATIC_URL}"
            "blog/img/posts/best-pricing-strategies-for-pilates-studios-in-2026/cover.jpg"
        )
    )


@pytest.mark.django_db
def test_post_fallback_cover_image_uses_default_when_missing():
    post = Post.objects.create(
        title="Slug sem imagem local",
        slug="slug-sem-imagem-local",
        content="Conteudo do artigo.",
        published=True,
    )

    assert post.fallback_cover_image == f"{settings.STATIC_URL}blog/img/posts/default/cover.jpg"


@pytest.mark.django_db
def test_post_display_cover_image_prefers_uploaded_file():
    post = Post.objects.create(
        title="Post com arquivo",
        cover_image="https://example.com/cover.jpg",
        cover_image_file=SimpleUploadedFile(
            "cover.jpg",
            (
                b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00"
                b"\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00"
                b"\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
            ),
            content_type="image/gif",
        ),
        content="Conteudo do artigo.",
        published=True,
    )

    assert post.display_cover_image.startswith(f"{settings.MEDIA_URL}blog/covers/")


@pytest.mark.django_db
def test_post_display_cover_image_uses_url_when_no_uploaded_file():
    post = Post.objects.create(
        title="Post com url",
        cover_image="https://example.com/cover.jpg",
        content="Conteudo do artigo.",
        published=True,
    )

    assert post.display_cover_image == "https://example.com/cover.jpg"


@pytest.mark.django_db
def test_post_ordering_prioritizes_featured_then_latest():
    older_featured = Post.objects.create(
        title="Destaque antigo",
        content="Conteudo",
        is_featured=True,
        published=True,
        published_at=timezone.now() - timezone.timedelta(days=2),
    )
    newer_featured = Post.objects.create(
        title="Destaque novo",
        content="Conteudo",
        is_featured=True,
        published=True,
        published_at=timezone.now() - timezone.timedelta(days=1),
    )
    newest_regular = Post.objects.create(
        title="Regular novo",
        content="Conteudo",
        is_featured=False,
        published=True,
        published_at=timezone.now(),
    )

    ordered_titles = list(Post.objects.values_list("title", flat=True))

    assert ordered_titles == [
        newer_featured.title,
        older_featured.title,
        newest_regular.title,
    ]
