# Generated by Django 4.1.1 on 2022-11-01 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0005_alter_propertycontact_subject"),
    ]

    operations = [
        migrations.RemoveField(model_name="propertycontact", name="subject",),
        migrations.AddField(
            model_name="propertycontact",
            name="property",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="property_contacts",
                to="properties.property",
            ),
            preserve_default=False,
        ),
    ]