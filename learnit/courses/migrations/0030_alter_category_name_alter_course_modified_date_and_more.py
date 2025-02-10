# Generated by Django 5.1.5 on 2025-02-10 04:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0029_alter_category_create_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(db_index=True, max_length=200),
        ),
        migrations.AlterField(
            model_name="course",
            name="modified_date",
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name="course",
            name="name",
            field=models.CharField(db_index=True, max_length=280),
        ),
    ]
