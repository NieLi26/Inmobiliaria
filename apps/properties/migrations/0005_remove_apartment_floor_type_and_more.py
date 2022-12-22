# Generated by Django 4.1.1 on 2022-12-13 21:04

import apps.properties.models
from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("properties", "0004_house_common_expenses_alter_house_distribution_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="apartment", name="floor_type",),
        migrations.RemoveField(model_name="apartment", name="is_furnished",),
        migrations.AddField(
            model_name="apartment",
            name="distribution",
            field=multiselectfield.db.fields.MultiSelectField(
                choices=[
                    ("Baño Visita", "Baño Visita"),
                    ("Hall", "Hall"),
                    ("Antejardin", "Antejardin"),
                    ("Patio de Servicio", "Patio de Servicio"),
                    ("Estar de Servicio", "Estar de Servicio"),
                    ("Jardin", "Jardin"),
                    ("Despensa", "Despensa"),
                    ("Sala Estar", "Sala Estar"),
                    ("Quincho", "Quincho"),
                    ("Lavadero Interior", "Lavadero Interior"),
                    ("Lavadero Exterior", "Lavadero Exterior"),
                    ("Escritorio", "Escritorio"),
                    ("Mansarda", "Mansarda"),
                    ("Terraza", "Terraza"),
                ],
                default="",
                max_length=250,
                verbose_name="Distribución",
            ),
        ),
        migrations.AddField(
            model_name="apartment",
            name="kitchen",
            field=multiselectfield.db.fields.MultiSelectField(
                choices=[
                    ("Comedor Diario", "Comedor Diario"),
                    ("Cocina Equipada", "Cocina Equipada"),
                    ("Cocina Amoblada", "Cocina Amoblada"),
                ],
                default="",
                max_length=250,
                verbose_name="Cocina",
            ),
        ),
        migrations.AddField(
            model_name="apartment",
            name="other",
            field=multiselectfield.db.fields.MultiSelectField(
                choices=[
                    ("Persianas", "Persianas"),
                    ("Protecciones Ventana", "Protecciones Ventana"),
                    ("Termopaneles", "Termopaneles"),
                ],
                default="",
                max_length=250,
                verbose_name="Otros",
            ),
        ),
        migrations.AddField(
            model_name="apartment",
            name="service",
            field=multiselectfield.db.fields.MultiSelectField(
                choices=[
                    ("Alarma", "Alarma"),
                    ("Jacuzzi", "Jacuzzi"),
                    ("Telefono", "Telefono"),
                    ("Riego Automatico", "Riego Automatico"),
                    ("Porton Automatico", "Porton Automatico"),
                    ("Piscina", "Piscina"),
                    ("TV Cable", "TV Cable"),
                    ("Chimenea", "Chimenea"),
                    ("Calefaccion", "Calefaccion"),
                    ("Aire Acondicionado", "Aire Acondicionado"),
                ],
                default="",
                max_length=250,
                verbose_name="Servicios",
            ),
        ),
        migrations.AlterField(
            model_name="house",
            name="builded_surface",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Superficie construida (m²)"
            ),
        ),
        migrations.AlterField(
            model_name="house",
            name="builded_year",
            field=models.PositiveIntegerField(
                blank=True, default=0, null=True, verbose_name="Año de Construcción"
            ),
        ),
        migrations.AlterField(
            model_name="house",
            name="common_expenses",
            field=models.PositiveIntegerField(default=0, verbose_name="Gastos comunes"),
        ),
        migrations.AlterField(
            model_name="house",
            name="num_bathrooms",
            field=models.PositiveIntegerField(default=0, verbose_name="Baños"),
        ),
        migrations.AlterField(
            model_name="house",
            name="num_cellars",
            field=models.PositiveIntegerField(
                blank=True, default=0, null=True, verbose_name="Bodegas"
            ),
        ),
        migrations.AlterField(
            model_name="house",
            name="num_floors",
            field=models.PositiveIntegerField(
                blank=True, default=0, null=True, verbose_name="Pisos"
            ),
        ),
        migrations.AlterField(
            model_name="house",
            name="num_house",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="Número Casa"
            ),
        ),
        migrations.AlterField(
            model_name="house",
            name="num_parkings",
            field=models.PositiveIntegerField(
                blank=True, default=0, null=True, verbose_name="Estacionamientos"
            ),
        ),
        migrations.AlterField(
            model_name="house",
            name="num_rooms",
            field=models.PositiveIntegerField(default=0, verbose_name="Dormitorios"),
        ),
        migrations.AlterField(
            model_name="property",
            name="description",
            field=models.TextField(verbose_name="Descripción"),
        ),
        migrations.AlterField(
            model_name="property",
            name="email",
            field=models.EmailField(
                blank=True, max_length=150, null=True, verbose_name="Correo"
            ),
        ),
        migrations.AlterField(
            model_name="property",
            name="land_surface",
            field=models.PositiveIntegerField(
                default=0, verbose_name="Superficie terreno (m²)"
            ),
        ),
        migrations.AlterField(
            model_name="property",
            name="phone1",
            field=models.CharField(blank=True, max_length=9, verbose_name="Telefono 1"),
        ),
        migrations.AlterField(
            model_name="property",
            name="phone2",
            field=models.CharField(blank=True, max_length=9, verbose_name="Telefono 2"),
        ),
        migrations.AlterField(
            model_name="property",
            name="price",
            field=models.PositiveIntegerField(default=0, verbose_name="Precio"),
        ),
        migrations.AlterField(
            model_name="property",
            name="property_type",
            field=models.CharField(
                choices=[
                    ("de", "Departamento"),
                    ("ca", "Casa"),
                    ("of", "Oficina"),
                    ("lc", "Local Comercial"),
                    ("su", "Sitio Urbano"),
                    ("pa", "Parcela"),
                    ("in", "Industrial"),
                    ("bo", "Bodega"),
                    ("es", "Estacionamiento"),
                    ("va", "Vacacional"),
                ],
                max_length=2,
                verbose_name="Tipo de Propiedad",
            ),
        ),
        migrations.AlterField(
            model_name="property",
            name="publish_type",
            field=models.CharField(
                choices=[
                    ("", "Seleccione un tipo"),
                    ("ve", "Venta"),
                    ("ar", "Arriendo"),
                    ("at", "Arriendo Temporada"),
                    ("pe", "Permuta"),
                ],
                max_length=2,
                verbose_name="Tipo de Operación",
            ),
        ),
        migrations.AlterField(
            model_name="property",
            name="street_address",
            field=models.CharField(max_length=50, verbose_name="Calle"),
        ),
        migrations.AlterField(
            model_name="property",
            name="street_number",
            field=models.PositiveIntegerField(verbose_name="Número"),
        ),
        migrations.AlterField(
            model_name="property",
            name="thumbnail",
            field=models.ImageField(
                blank=True,
                upload_to=apps.properties.models.property_directory_path,
                verbose_name="Imagen",
            ),
        ),
        migrations.AlterField(
            model_name="property",
            name="title",
            field=models.CharField(
                max_length=100, verbose_name="Titulo(hasta 100 caracteres)"
            ),
        ),
        migrations.AlterField(
            model_name="property",
            name="type_price",
            field=models.CharField(
                choices=[
                    ("", "Seleccione un tipo"),
                    ("uf", "UF"),
                    ("usd", "USD"),
                    ("clp", "CLP"),
                ],
                max_length=3,
                verbose_name="Tipo Moneda",
            ),
        ),
    ]
