# Generated by Django 5.1.5 on 2025-02-01 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0017_remove_lesson_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='url',
            field=models.URLField(unique=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='video_id',
            field=models.CharField(),
        ),
    ]
