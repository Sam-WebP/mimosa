# Generated by Django 5.0.3 on 2024-06-16 05:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_order"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="certificate",
        ),
        migrations.CreateModel(
            name="OrderLine",
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
                (
                    "certificate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.certificate",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.order",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="order",
            name="certificate",
            field=models.ManyToManyField(
                through="core.OrderLine", to="core.certificate"
            ),
        ),
    ]
