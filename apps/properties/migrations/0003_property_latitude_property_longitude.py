# Generated by Django 4.1.1 on 2022-10-18 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0002_property_google_url_property_is_featured_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="property",
            name="latitude",
            field=models.CharField(blank=True, max_length=250, verbose_name="Latitud"),
        ),
        migrations.AddField(
            model_name="property",
            name="longitude",
            field=models.CharField(blank=True, max_length=250, verbose_name="Longitud"),
        ),
    ]
