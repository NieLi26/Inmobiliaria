# Generated by Django 4.1.1 on 2022-10-31 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0002_alter_contact_subject"),
    ]

    operations = [
        migrations.CreateModel(
            name="OwnerContact",
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
                    "name",
                    models.CharField(max_length=200, verbose_name="Nombre Completo"),
                ),
                ("from_email", models.EmailField(max_length=50, verbose_name="Email")),
                ("subject", models.CharField(max_length=100, verbose_name="Asunto")),
                (
                    "phone",
                    models.CharField(
                        blank=True, max_length=9, verbose_name="Télefono(opcional)"
                    ),
                ),
                ("message", models.TextField(verbose_name="Mensaje")),
            ],
            options={
                "verbose_name": "OwnerContact",
                "verbose_name_plural": "OwnerContacts",
            },
        ),
    ]
