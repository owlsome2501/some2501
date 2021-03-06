# Generated by Django 2.2.2 on 2019-07-02 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="artical",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file_name", models.CharField(max_length=256)),
                ("title", models.CharField(max_length=256)),
                ("pub_time", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="author",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
                ("mail", models.EmailField(blank=True, max_length=254, null=True)),
                ("nickname", models.CharField(blank=True, max_length=30, null=True)),
                ("description", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="md_cache",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("update_time", models.DateTimeField()),
                ("file_path", models.CharField(max_length=512)),
            ],
        ),
        migrations.DeleteModel(name="artical_cache",),
        migrations.AddField(
            model_name="artical",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="blog.author"
            ),
        ),
        migrations.AddField(
            model_name="artical",
            name="content",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="blog.md_cache"
            ),
        ),
    ]
