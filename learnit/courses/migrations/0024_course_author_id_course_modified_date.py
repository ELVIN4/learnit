# Generated by Django 5.1.5 on 2025-02-04 00:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0023_category_is_published"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="author_id",
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name="course",
            name="modified_date",
            field=models.DateField(null=True, blank=True),
        ),
    ]
