# Generated by Django 4.2.6 on 2023-11-28 06:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fetch_data", "0026_alter_queuedtask_time_queued"),
    ]

    operations = [
        migrations.AlterField(
            model_name="queuedtask",
            name="time_queued",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 11, 28, 13, 59, 1, 345223)
            ),
        ),
    ]