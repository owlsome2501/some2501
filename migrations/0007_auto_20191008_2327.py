# Generated by Django 2.2.2 on 2019-10-08 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_md_cache_raw_content"),
    ]

    operations = [
        migrations.CreateModel(
            name="tag",
            fields=[("text", models.TextField(primary_key=True, serialize=False)),],
        ),
        migrations.AddField(
            model_name="article",
            name="tags",
            field=models.ManyToManyField(to="blog.tag"),
        ),
    ]
