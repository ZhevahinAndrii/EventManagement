# Generated by Django 5.1.6 on 2025-02-20 14:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
