# Generated by Django 5.1.5 on 2025-02-05 02:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0024_course_author_id_course_modified_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="language",
            name="code",
            field=models.CharField(default="ru", max_length=2),
        ),
    ]
