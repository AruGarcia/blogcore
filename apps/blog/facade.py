from apps.blog.models import Post


def list_published_posts_ordered():
    return Post.objects.filter(published=True).order_by("-published_at", "-created_at")


def find_featured_post():
    posts = list_published_posts_ordered()
    return posts.filter(is_featured=True).first() or posts.first()


def find_published_post(slug):
    return Post.objects.get(slug=slug, published=True)


def list_related_articles(post, limit=3):
    return list_published_posts_ordered().exclude(pk=post.pk)[:limit]
