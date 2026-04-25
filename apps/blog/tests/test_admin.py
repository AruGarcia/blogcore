from django.contrib.admin.sites import site

from apps.blog.admin import PostAdmin
from apps.blog.models import Post


def test_post_admin_configuration():
    assert PostAdmin.list_display == (
        "title",
        "is_featured",
        "published",
        "published_at",
        "updated_at",
    )
    assert PostAdmin.list_filter == (
        "published",
        "is_featured",
        "created_at",
        "published_at",
    )
    assert PostAdmin.search_fields == ("title", "excerpt", "content")
    assert PostAdmin.prepopulated_fields == {"slug": ("title",)}
    assert PostAdmin.list_editable == ("is_featured", "published")
    assert PostAdmin.date_hierarchy == "published_at"


def test_post_is_registered_in_admin_site():
    assert Post in site._registry
