# Generated by Django 4.2.6 on 2023-11-25 08:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("fetch_data", "0015_rename_queuedtasks_queuedtask_detectedobject_task"),
    ]

    operations = [
        migrations.RenameField(
            model_name="satteliteimage",
            old_name="Area_tag",
            new_name="area_tag",
        ),
    ]
