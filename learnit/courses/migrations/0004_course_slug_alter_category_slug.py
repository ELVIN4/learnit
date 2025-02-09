# Generated by Django 5.1.5 on 2025-01-26 19:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0003_alter_course_update_time_alter_course_upload_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="slug",
            field=models.SlugField(null=True),
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(max_length=140),
        ),
    ]
