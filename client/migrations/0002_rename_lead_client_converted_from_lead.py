# Generated by Django 5.2 on 2025-05-14 17:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("client", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="client",
            old_name="lead",
            new_name="converted_from_lead",
        ),
    ]
