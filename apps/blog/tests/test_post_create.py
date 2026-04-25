import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from apps.blog.models import Post


@pytest.mark.django_db
def test_post_create_returns_success(client):
    response = client.get(reverse("post_create"))
    template_names = [template.name for template in response.templates if template.name]

    assert response.status_code == 200
    assert "blog/post_form.html" in template_names


@pytest.mark.django_db
def test_post_create_renders_form_fields(client):
    response = client.get(reverse("post_create"))
    content = response.content.decode()

    assert "Create a new blog post" in content
    assert 'name="title"' in content
    assert 'name="excerpt"' in content
    assert 'name="cover_image"' in content
    assert 'name="cover_image_file"' in content
    assert 'name="content"' in content
    assert 'name="published"' in content
    assert 'name="is_featured"' in content
    assert 'enctype="multipart/form-data"' in content


@pytest.mark.django_db
def test_post_create_renders_ckeditor_widget(client):
    response = client.get(reverse("post_create"))
    content = response.content.decode()

    assert 'django_ckeditor_5/dist/styles.css' in content
    assert 'django_ckeditor_5/dist/bundle.js' in content
    assert 'class="django_ckeditor_5 blog-ckeditor' in content
    assert 'data-upload-url="/ckeditor5/image_upload/"' in content


@pytest.mark.django_db
def test_post_create_creates_published_post_and_redirects_to_detail(client):
    response = client.post(
        reverse("post_create"),
        data={
            "title": "Novo post pelo site",
            "excerpt": "Resumo do novo post.",
            "cover_image": "https://example.com/post.jpg",
            "content": "Conteudo do novo post.",
            "published": "on",
            "is_featured": "on",
            "published_at": "2026-04-25T10:30",
        },
    )

    post = Post.objects.get(title="Novo post pelo site")

    assert response.status_code == 302
    assert response.url == post.get_absolute_url()
    assert post.slug == "novo-post-pelo-site"
    assert post.is_featured is True
    assert post.published is True


@pytest.mark.django_db
def test_post_create_creates_unpublished_post_and_redirects_home(client):
    response = client.post(
        reverse("post_create"),
        data={
            "title": "Rascunho pelo site",
            "excerpt": "Resumo do rascunho.",
            "cover_image": "",
            "content": "Conteudo do rascunho.",
        },
    )

    post = Post.objects.get(title="Rascunho pelo site")

    assert response.status_code == 302
    assert response.url == reverse("home")
    assert post.published is False


@pytest.mark.django_db
def test_post_create_shows_validation_errors(client):
    response = client.post(
        reverse("post_create"),
        data={
            "title": "",
            "content": "",
        },
    )

    assert response.status_code == 200
    assert Post.objects.count() == 0
    assert "This field is required." in response.content.decode()


@pytest.mark.django_db
def test_post_create_accepts_uploaded_cover_image(client, settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path

    response = client.post(
        reverse("post_create"),
        data={
            "title": "Post com upload",
            "excerpt": "Resumo com upload.",
            "cover_image": "",
            "cover_image_file": SimpleUploadedFile(
                "cover.gif",
                (
                    b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00"
                    b"\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00"
                    b"\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b"
                ),
                content_type="image/gif",
            ),
            "content": "Conteudo com upload.",
            "published": "on",
        },
    )

    post = Post.objects.get(title="Post com upload")

    assert response.status_code == 302
    assert post.cover_image_file.name
