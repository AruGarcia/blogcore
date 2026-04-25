from django.shortcuts import get_object_or_404, render

from .models import Post


def home(request):
    posts = Post.objects.filter(published=True)
    featured_article = posts.filter(is_featured=True).first() or posts.first()
    articles = posts.order_by("-published_at", "-created_at")

    context = {
        "featured_article": featured_article,
        "articles": articles,
    }
    return render(request, "blog/home.html", context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    related_articles = (
        Post.objects.filter(published=True)
        .exclude(pk=post.pk)
        .order_by("-published_at", "-created_at")[:3]
    )

    context = {
        "post": post,
        "related_articles": related_articles,
    }
    return render(request, "blog/post_detail.html", context)
