# Generated by Django 4.2.6 on 2023-11-26 13:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fetch_data", "0020_queuedtask_is_parent"),
    ]

    operations = [
        migrations.AddField(
            model_name="queuedtask",
            name="childs_task_ids",
            field=models.TextField(null=True),
        ),
    ]