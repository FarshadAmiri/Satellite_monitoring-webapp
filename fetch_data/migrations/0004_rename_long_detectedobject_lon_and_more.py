# Generated by Django 4.2.6 on 2023-11-13 04:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("fetch_data", "0003_detectedobject_watercraft_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="detectedobject",
            old_name="long",
            new_name="lon",
        ),
        migrations.RenameField(
            model_name="detectedobject",
            old_name="z",
            new_name="zoom",
        ),
        migrations.AddField(
            model_name="watercraft",
            name="watercraft_type",
            field=models.CharField(default="Shipcraft", max_length=64),
        ),
        migrations.AlterField(
            model_name="detectedobject",
            name="id",
            field=models.CharField(max_length=128, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="detectedobject",
            name="object_type",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="detected_objects",
                to="fetch_data.watercraft",
            ),
        ),
        migrations.AlterField(
            model_name="watercraft",
            name="color",
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name="watercraft",
            name="length_max",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="watercraft",
            name="length_min",
            field=models.FloatField(null=True),
        ),
    ]
