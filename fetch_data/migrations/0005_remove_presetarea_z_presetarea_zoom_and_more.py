# Generated by Django 4.2.6 on 2023-11-05 08:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fetch_data", "0004_rename_presetareas_presetarea_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="presetarea",
            name="z",
        ),
        migrations.AddField(
            model_name="presetarea",
            name="zoom",
            field=models.FloatField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(50),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="presetarea",
            name="description",
            field=models.TextField(blank=True, max_length=800, null=True),
        ),
        migrations.AlterField(
            model_name="presetarea",
            name="tag",
            field=models.CharField(
                max_length=128, primary_key=True, serialize=False, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="presetarea",
            name="x_max",
            field=models.FloatField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(500000),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="presetarea",
            name="x_min",
            field=models.FloatField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(500000),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="presetarea",
            name="y_max",
            field=models.FloatField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(500000),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="presetarea",
            name="y_min",
            field=models.FloatField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(500000),
                ],
            ),
        ),
    ]
