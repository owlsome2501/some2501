# Generated by Django 2.2.2 on 2019-08-04 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20190703_0848'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='artical',
            new_name='article',
        ),
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-pub_time']},
        ),
    ]
