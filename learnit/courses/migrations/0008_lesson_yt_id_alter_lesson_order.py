# Generated by Django 5.1.5 on 2025-01-30 01:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0007_alter_lesson_options_lesson_order"),
    ]

    operations = [
        migrations.AddField(
            model_name="lesson",
            name="yt_id",
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="order",
            field=models.PositiveIntegerField(blank=True, default=1),
        ),
    ]
