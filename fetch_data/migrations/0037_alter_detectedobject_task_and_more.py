# Generated by Django 4.2.6 on 2023-12-10 09:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fetch_data", "0036_queuedtask_confidence_threshold"),
    ]

    operations = [
        migrations.AlterField(
            model_name="detectedobject",
            name="task",
            field=models.ManyToManyField(
                related_name="detected_objects", to="fetch_data.queuedtask"
            ),
        ),
        migrations.AlterField(
            model_name="queuedtask",
            name="child_task",
            field=models.ManyToManyField(
                related_name="parent_task", to="fetch_data.queuedtask"
            ),
        ),
    ]