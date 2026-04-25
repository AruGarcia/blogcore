import pytest
from django.utils import timezone

from apps.blog import facade
from apps.blog.models import Post


@pytest.fixture
def published_posts(db):
    older = Post.objects.create(
        title="Older post",
        content="Older content.",
        published=True,
        published_at=timezone.now() - timezone.timedelta(days=2),
    )
    featured = Post.objects.create(
        title="Featured post",
        content="Featured content.",
        is_featured=True,
        published=True,
        published_at=timezone.now() - timezone.timedelta(days=1),
    )
    newest = Post.objects.create(
        title="Newest post",
        content="Newest content.",
        published=True,
        published_at=timezone.now(),
    )
    Post.objects.create(
        title="Draft post",
        content="Draft content.",
        published=False,
    )
    return older, featured, newest


@pytest.mark.django_db
def test_list_published_posts_ordered(published_posts):
    older, featured, newest = published_posts

    assert list(facade.list_published_posts_ordered()) == [newest, featured, older]


@pytest.mark.django_db
def test_find_featured_post(published_posts):
    _, featured, _ = published_posts

    assert facade.find_featured_post() == featured


@pytest.mark.django_db
def test_find_published_post(published_posts):
    _, featured, _ = published_posts

    assert facade.find_published_post(featured.slug) == featured


@pytest.mark.django_db
def test_list_related_articles_excludes_current_post_and_limits_results(published_posts):
    older, featured, newest = published_posts

    assert list(facade.list_related_articles(featured, limit=2)) == [newest, older]
