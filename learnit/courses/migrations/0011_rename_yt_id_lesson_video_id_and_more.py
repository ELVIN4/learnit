# Generated by Django 5.1.5 on 2025-01-30 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_remove_course_update_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='yt_id',
            new_name='video_id',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='lesson_url',
        ),
        migrations.AddField(
            model_name='lesson',
            name='author',
            field=models.CharField(default=None),
        ),
        migrations.AddField(
            model_name='lesson',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='lesson',
            name='thumbnail_url',
            field=models.URLField(default=None),
        ),
        migrations.AddField(
            model_name='lesson',
            name='upload_date',
            field=models.DateTimeField(blank=True, default=None),
        ),
        migrations.AddField(
            model_name='lesson',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
