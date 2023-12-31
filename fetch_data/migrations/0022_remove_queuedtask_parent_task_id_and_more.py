# Generated by Django 4.2.6 on 2023-11-27 04:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fetch_data", "0021_queuedtask_childs_task_ids"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="queuedtask",
            name="parent_task_id",
        ),
        migrations.RemoveField(
            model_name="queuedtask",
            name="childs_task_ids",
        ),
        migrations.AddField(
            model_name="queuedtask",
            name="childs_task_ids",
            field=models.ManyToManyField(
                null=True, related_name="parent_task", to="fetch_data.queuedtask"
            ),
        ),
    ]
