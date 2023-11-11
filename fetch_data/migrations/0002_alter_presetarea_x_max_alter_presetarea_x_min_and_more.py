# Generated by Django 4.2.6 on 2023-11-11 04:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fetch_data", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="presetarea",
            name="x_max",
            field=models.IntegerField(
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
            field=models.IntegerField(
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
            field=models.IntegerField(
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
            field=models.IntegerField(
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
            name="zoom",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(50),
                ],
            ),
        ),
    ]