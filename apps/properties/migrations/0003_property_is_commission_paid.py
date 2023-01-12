# Generated by Django 4.1.1 on 2023-01-03 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "properties",
            "0002_alter_apartment_distribution_alter_apartment_kitchen_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="property",
            name="is_commission_paid",
            field=models.BooleanField(default=False, verbose_name="Comisión Pagada"),
        ),
    ]
