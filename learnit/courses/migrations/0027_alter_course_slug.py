# Generated by Django 5.1.5 on 2025-02-07 00:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0026_alter_language_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="slug",
            field=models.SlugField(max_length=300, null=True),
        ),
    ]
