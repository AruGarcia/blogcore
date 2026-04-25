from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_post_editorial_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="cover_image_file",
            field=models.ImageField(
                blank=True,
                upload_to="blog/covers/%Y/%m/",
                verbose_name="arquivo da imagem de capa",
            ),
        ),
    ]
