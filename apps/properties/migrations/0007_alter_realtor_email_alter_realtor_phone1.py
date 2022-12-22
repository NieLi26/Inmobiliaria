# Generated by Django 4.1.1 on 2022-12-14 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "properties",
            "0006_realtor_remove_property_email_remove_property_phone1_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="realtor",
            name="email",
            field=models.EmailField(default=0, max_length=150, verbose_name="Correo"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="realtor",
            name="phone1",
            field=models.CharField(max_length=9, verbose_name="Telefono 1"),
        ),
    ]
