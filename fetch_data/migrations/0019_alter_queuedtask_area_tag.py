# Generated by Django 4.2.6 on 2023-11-26 08:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "fetch_data",
            "0018_queuedtask_parent_task_id_remove_queuedtask_area_tag_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="queuedtask",
            name="area_tag",
            field=models.ManyToManyField(to="fetch_data.presetarea"),
        ),
    ]
