# Generated by Django 2.2.2 on 2019-07-03 00:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190703_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artical',
            name='content',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blog.md_cache'),
        ),
        migrations.AlterField(
            model_name='author',
            name='description',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blog.md_cache'),
        ),
    ]
