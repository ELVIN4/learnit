# Generated by Django 5.1.5 on 2025-02-02 00:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0022_alter_course_update_date_alter_course_upload_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="is_published",
            field=models.BooleanField(default=True),
        ),
    ]
