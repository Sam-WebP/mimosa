# Generated by Django 5.0.3 on 2024-07-24 20:35

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0022_order_order_hash"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="order_hash",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, unique=True
            ),
        ),
    ]
