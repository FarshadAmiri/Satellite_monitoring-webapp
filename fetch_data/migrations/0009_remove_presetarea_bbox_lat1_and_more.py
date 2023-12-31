# Generated by Django 4.2.6 on 2023-11-20 09:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fetch_data", "0008_alter_queuedtasks_task_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="presetarea",
            name="bbox_lat1",
        ),
        migrations.RemoveField(
            model_name="presetarea",
            name="bbox_lat2",
        ),
        migrations.RemoveField(
            model_name="presetarea",
            name="bbox_lon1",
        ),
        migrations.RemoveField(
            model_name="presetarea",
            name="bbox_lon2",
        ),
        migrations.RemoveField(
            model_name="presetarea",
            name="x_max",
        ),
        migrations.RemoveField(
            model_name="presetarea",
            name="x_min",
        ),
        migrations.RemoveField(
            model_name="presetarea",
            name="y_max",
        ),
        migrations.RemoveField(
            model_name="presetarea",
            name="y_min",
        ),
        migrations.RemoveField(
            model_name="presetarea",
            name="zoom",
        ),
        migrations.AddField(
            model_name="presetarea",
            name="lat_max",
            field=models.FloatField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(-90),
                    django.core.validators.MaxValueValidator(90),
                ],
            ),
        ),
        migrations.AddField(
            model_name="presetarea",
            name="lat_min",
            field=models.FloatField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(-90),
                    django.core.validators.MaxValueValidator(90),
                ],
            ),
        ),
        migrations.AddField(
            model_name="presetarea",
            name="lon_max",
            field=models.FloatField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(-180),
                    django.core.validators.MaxValueValidator(180),
                ],
            ),
        ),
        migrations.AddField(
            model_name="presetarea",
            name="lon_min",
            field=models.FloatField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(-180),
                    django.core.validators.MaxValueValidator(180),
                ],
            ),
        ),
    ]
