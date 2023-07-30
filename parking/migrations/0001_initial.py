# Generated by Django 4.1.5 on 2023-07-30 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ParkingModel",
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
                ("name", models.CharField(max_length=64)),
                ("latitude", models.DecimalField(decimal_places=8, max_digits=180)),
                ("longitude", models.DecimalField(decimal_places=8, max_digits=180)),
                ("capacity", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="ParkingSpot",
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
                ("number", models.CharField(max_length=32)),
                ("owner", models.CharField(max_length=16)),
                ("occupied", models.BooleanField(default=False)),
                ("is_reservable", models.BooleanField(default=False)),
                (
                    "parking",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="parking.parkingmodel",
                    ),
                ),
            ],
        ),
    ]
