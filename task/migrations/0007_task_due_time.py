# Generated by Django 5.2 on 2025-07-01 12:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("task", "0006_alter_task_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="due_time",
            field=models.TimeField(blank=True, null=True),
        ),
    ]
