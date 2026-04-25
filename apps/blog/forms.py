from django import forms
from django.utils import timezone
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Post


class PostForm(forms.ModelForm):
    published_at = forms.DateTimeField(
        label="Publish date",
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control blog-form-control",
            },
        ),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    class Meta:
        model = Post
        fields = (
            "title",
            "excerpt",
            "cover_image",
            "cover_image_file",
            "content",
            "is_featured",
            "published",
            "published_at",
        )
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control blog-form-control",
                    "placeholder": "Enter the article title",
                }
            ),
            "excerpt": forms.Textarea(
                attrs={
                    "class": "form-control blog-form-control",
                    "rows": 3,
                    "placeholder": "Short summary for the blog home and article page",
                }
            ),
            "cover_image": forms.URLInput(
                attrs={
                    "class": "form-control blog-form-control",
                    "placeholder": "https://...",
                }
            ),
            "cover_image_file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control blog-form-control",
                    "accept": "image/*",
                }
            ),
            "content": forms.Textarea(
                attrs={"class": "blog-richtext-source"}
            ),
            "is_featured": forms.CheckboxInput(
                attrs={"class": "form-check-input blog-form-check-input"}
            ),
            "published": forms.CheckboxInput(
                attrs={"class": "form-check-input blog-form-check-input"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].widget = CKEditor5Widget(
            config_name="default",
            attrs={"class": "django_ckeditor_5 blog-ckeditor"},
        )
        self.fields["title"].label = "Title"
        self.fields["title"].widget.attrs["placeholder"] = "Enter the article title"
        self.fields["excerpt"].label = "Excerpt"
        self.fields["excerpt"].widget.attrs["placeholder"] = (
            "Short summary for the blog home and article page"
        )
        self.fields["cover_image"].label = "Cover image URL"
        self.fields["cover_image"].widget.attrs["placeholder"] = "https://..."
        self.fields["cover_image_file"].label = "Upload cover image"
        self.fields["content"].label = "Article content"
        self.fields["published"].label = "Publish now"
        self.fields["is_featured"].label = "Mark as featured"
        for name, field in self.fields.items():
            if name not in {"is_featured", "published"}:
                field.widget.attrs.setdefault("class", "form-control blog-form-control")

    def clean_published_at(self):
        return self.cleaned_data["published_at"] or timezone.now()
