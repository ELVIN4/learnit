# Generated by Django 5.1.5 on 2025-01-30 02:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0009_alter_lesson_order_alter_lesson_yt_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="course",
            name="update_time",
        ),
    ]
