# Generated by Django 4.0.6 on 2022-09-28 00:43

import apps.properties.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commune',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified', models.DateField(auto_now=True, verbose_name='Fecha de Modificaión')),
                ('name', models.CharField(max_length=150, verbose_name='Comuna')),
                ('location_slug', models.SlugField()),
            ],
            options={
                'verbose_name': 'Commune',
                'verbose_name_plural': 'Communes',
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified', models.DateField(auto_now=True, verbose_name='Fecha de Modificaión')),
                ('property_type', models.CharField(choices=[('de', 'Departamento'), ('ca', 'Casa'), ('of', 'Oficina'), ('lc', 'Local Comercial'), ('su', 'Sitio Urbano'), ('pa', 'Parcela'), ('in', 'Industrial'), ('bo', 'Bodega'), ('es', 'Estacionamiento'), ('va', 'Vacacional')], max_length=2, verbose_name='Tipo de Propiedad*')),
                ('publish_type', models.CharField(choices=[('ve', 'Venta'), ('ar', 'Arriendo'), ('at', 'Arriendo Temporada')], max_length=2, verbose_name='Tipo de Operación*')),
                ('land_surface', models.PositiveIntegerField(verbose_name='Superficie terreno (m²)*')),
                ('title', models.CharField(max_length=150, verbose_name='Titulo*')),
                ('description', models.TextField(verbose_name='Descripción*')),
                ('type_price', models.CharField(choices=[('uf', 'UF'), ('clp', '$')], max_length=3, verbose_name='Tipo Precio*')),
                ('price', models.PositiveIntegerField(verbose_name='Precio*')),
                ('thumbnail', models.ImageField(blank=True, upload_to=apps.properties.models.property_directory_path, verbose_name='Imagen (Opcional)')),
                ('street_address', models.CharField(max_length=50, verbose_name='Calle*')),
                ('street_number', models.CharField(max_length=50, verbose_name='Número*')),
                ('phone1', models.CharField(blank=True, max_length=9, verbose_name='Telefono 1 (Opcional)')),
                ('phone2', models.CharField(blank=True, max_length=9, verbose_name='Telefono 2 (Opcional)')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('commune', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='properties.commune', verbose_name='Comuna*')),
            ],
            options={
                'verbose_name': 'Property',
                'verbose_name_plural': 'Properties',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified', models.DateField(auto_now=True, verbose_name='Fecha de Modificaión')),
                ('name', models.CharField(max_length=150, verbose_name='Comuna')),
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': 'Regions',
            },
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified', models.DateField(auto_now=True, verbose_name='Fecha de Modificaión')),
                ('image', models.ImageField(upload_to=apps.properties.models.property_images_directory_path)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='properties.property')),
            ],
            options={
                'verbose_name': 'PropertyImage',
                'verbose_name_plural': 'PropertyImages',
            },
        ),
        migrations.AddField(
            model_name='property',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='properties.region', verbose_name='Región*'),
        ),
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified', models.DateField(auto_now=True, verbose_name='Fecha de Modificaión')),
                ('builded_surface', models.PositiveIntegerField(verbose_name='Superficie construida (m²)*')),
                ('num_rooms', models.PositiveBigIntegerField(verbose_name='Dormitorios*')),
                ('num_bathrooms', models.PositiveIntegerField(verbose_name='Baños*')),
                ('floor_type', models.CharField(max_length=150, verbose_name='Tipo piso*')),
                ('is_furnished', models.BooleanField(default=False, verbose_name='Esta propiedad está amoblada*')),
                ('num_parkings', models.PositiveIntegerField(blank=True, null=True, verbose_name='Estacionamientos (Opcional)')),
                ('num_cellars', models.PositiveIntegerField(blank=True, null=True, verbose_name='Bodegas (Opcional)')),
                ('num_floors', models.PositiveIntegerField(blank=True, null=True, verbose_name='Pisos (Opcional)')),
                ('num_house', models.CharField(blank=True, max_length=20, null=True, verbose_name='Número casa (Opcional)')),
                ('builded_year', models.PositiveIntegerField(blank=True, null=True, verbose_name='Año de Construcción (Opcional)')),
                ('property', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='houses', to='properties.property')),
            ],
            options={
                'verbose_name': 'House',
                'verbose_name_plural': 'Houses',
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='commune',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='communes', to='properties.region'),
        ),
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(default=True, verbose_name='Estado')),
                ('created', models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('modified', models.DateField(auto_now=True, verbose_name='Fecha de Modificaión')),
                ('builded_surface', models.PositiveIntegerField(verbose_name='Superficie construida (m²)*')),
                ('num_rooms', models.PositiveBigIntegerField(verbose_name='Dormitorios*')),
                ('num_bathrooms', models.PositiveIntegerField(verbose_name='Baños*')),
                ('floor_type', models.CharField(max_length=150, verbose_name='Tipo piso*')),
                ('is_furnished', models.BooleanField(default=False, verbose_name='Esta propiedad está amoblada*')),
                ('num_parkings', models.PositiveIntegerField(blank=True, null=True, verbose_name='Estacionamientos (Opcional)')),
                ('num_cellars', models.PositiveIntegerField(blank=True, null=True, verbose_name='Bodegas (Opcional)')),
                ('num_floors', models.PositiveIntegerField(blank=True, null=True, verbose_name='Pisos (Opcional)')),
                ('num_apartment', models.CharField(blank=True, max_length=20, null=True, verbose_name='Número depto (Opcional)')),
                ('builded_year', models.PositiveIntegerField(blank=True, null=True, verbose_name='Año de Construcción (Opcional)')),
                ('common_expenses', models.PositiveIntegerField(verbose_name='Gastos comunes*')),
                ('property', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='apartments', to='properties.property')),
            ],
            options={
                'verbose_name': 'Apartment',
                'verbose_name_plural': 'Apartments',
                'ordering': ('-created',),
            },
        ),
    ]
