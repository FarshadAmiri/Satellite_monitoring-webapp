# Generated by Django 4.2.6 on 2023-11-28 06:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fetch_data", "0024_rename_childs_tasks_queuedtask_child_task"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="detectedobject",
            name="task",
        ),
        migrations.AddField(
            model_name="detectedobject",
            name="task",
            field=models.ManyToManyField(
                null=True, related_name="detected_objects", to="fetch_data.queuedtask"
            ),
        ),
    ]
