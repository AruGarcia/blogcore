from apps.blog.apps import BlogConfig


def test_blog_app_config():
    assert BlogConfig.default_auto_field == "django.db.models.BigAutoField"
    assert BlogConfig.name == "apps.blog"
    assert BlogConfig.label == "blog"
