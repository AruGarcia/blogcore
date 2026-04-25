from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "published", "published_at", "updated_at")
    list_filter = ("published", "is_featured", "created_at", "published_at")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-is_featured", "-published_at", "-created_at")
    list_editable = ("is_featured", "published")
    date_hierarchy = "published_at"

    fieldsets = (
        ("Publicacao", {"fields": ("title", "slug", "excerpt", "content")}),
        ("Exibicao", {"fields": ("cover_image", "cover_image_file", "is_featured")}),
        ("Status", {"fields": ("published", "published_at")}),
    )
