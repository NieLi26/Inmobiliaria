# Generated by Django 4.1.1 on 2023-01-05 04:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        (
            "properties",
            "0005_rename_commission_price_propertymanager_commission_value_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(model_name="propertymanager", name="price",),
        migrations.RemoveField(model_name="propertymanager", name="type_price",),
        migrations.RemoveField(model_name="propertymanager", name="type_property",),
        migrations.AddField(
            model_name="propertymanager",
            name="total",
            field=models.CharField(
                default=django.utils.timezone.now, max_length=100, verbose_name="Total"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="propertymanager",
            name="commission_value",
            field=models.PositiveIntegerField(),
        ),
    ]