# Generated by Django 5.0.3 on 2024-07-08 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_ordersession_stripe_session_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="ordersession",
            old_name="stripe_session_id",
            new_name="stripe_checkout_id",
        ),
    ]
