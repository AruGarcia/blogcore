from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from . import facade
from .forms import PostForm
from .models import Post


def home(request):
    featured_article = facade.find_featured_post()
    articles = facade.list_published_posts_ordered()

    context = {
        "featured_article": featured_article,
        "articles": articles,
    }
    return render(request, "blog/home.html", context)


def post_detail(request, slug):
    try:
        post = facade.find_published_post(slug)
    except Post.DoesNotExist as exc:
        raise Http404() from exc
    related_articles = facade.list_related_articles(post)

    context = {
        "post": post,
        "related_articles": related_articles,
    }
    return render(request, "blog/post_detail.html", context)


def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            messages.success(request, "Post created successfully.")
            if post.published:
                return redirect(post.get_absolute_url())
            return redirect("home")
    else:
        form = PostForm()

    return render(
        request,
        "blog/post_form.html",
        {
            "form": form,
            "form_title": "Create a new blog post",
            "form_intro": "Use the fields below to draft and publish directly from the site.",
            "submit_label": "Save post",
        },
    )


def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, "Post updated successfully.")
            if post.published:
                return redirect(post.get_absolute_url())
            return redirect("home")
    else:
        form = PostForm(instance=post)

    return render(
        request,
        "blog/post_form.html",
        {
            "form": form,
            "post": post,
            "form_title": "Edit blog post",
            "form_intro": "Update the article content, cover image and publication settings.",
            "submit_label": "Update post",
        },
    )
