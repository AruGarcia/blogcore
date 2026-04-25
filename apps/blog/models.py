from pathlib import Path

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Post(models.Model):
    title = models.CharField("titulo", max_length=200)
    slug = models.SlugField("slug", unique=True, blank=True)
    excerpt = models.TextField("resumo", max_length=255, blank=True)
    cover_image = models.URLField("imagem de capa", blank=True)
    cover_image_file = models.ImageField(
        "arquivo da imagem de capa",
        upload_to="blog/covers/%Y/%m/",
        blank=True,
    )
    content = models.TextField("conteudo")
    is_featured = models.BooleanField("destaque", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField("publicado em", default=timezone.now)
    published = models.BooleanField("publicado", default=True)

    class Meta:
        ordering = ["-is_featured", "-published_at", "-created_at"]
        verbose_name = "publicacao"
        verbose_name_plural = "publicacoes"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def fallback_cover_image(self):
        relative_path = Path("blog/img/posts") / self.slug / "cover.jpg"
        absolute_path = (
            Path(settings.BASE_DIR) / "apps" / "blog" / "static" / relative_path
        )

        if absolute_path.exists():
            return f"{settings.STATIC_URL}{relative_path.as_posix()}"

        return f"{settings.STATIC_URL}blog/img/posts/default/cover.jpg"

    @property
    def display_cover_image(self):
        if self.cover_image_file:
            return self.cover_image_file.url
        if self.cover_image:
            return self.cover_image
        return self.fallback_cover_image

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title
