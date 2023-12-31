# Generated by Django 4.1.5 on 2023-08-04 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("parking", "0002_remove_parkingspotmodel_is_reservable_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AvailabilityModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("available_from", models.DateTimeField()),
                ("available_to", models.DateTimeField()),
                (
                    "cost_per_hour",
                    models.DecimalField(decimal_places=2, max_digits=4),
                ),
                (
                    "parking_spot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="availabilty",
                        to="parking.parkingspotmodel",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="AvailabiltyModel",
        ),
    ]
