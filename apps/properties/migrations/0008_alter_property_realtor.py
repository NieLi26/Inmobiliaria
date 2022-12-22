# Generated by Django 4.1.1 on 2022-12-15 02:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0007_alter_realtor_email_alter_realtor_phone1"),
    ]

    operations = [
        migrations.AlterField(
            model_name="property",
            name="realtor",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="properties",
                to="properties.realtor",
            ),
            preserve_default=False,
        ),
    ]