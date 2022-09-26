import uuid 
from django.db import models
from core.settings import MEDIA_URL, STATIC_URL
from django.urls import reverse
# from django.db.models.signals import post_save

from apps.base.models import TimeStampedModel

def property_directory_path(instance,filename):
    return 'property/{0}/{1}'.format(instance.street_address, filename)

def property_images_directory_path(instance,filename):
    return 'property_images/{0}/{1}'.format(instance.property.street_address, filename)

class Property(TimeStampedModel):
    '''Model definition for Property.'''

    PROPERTY_APARTMENT = 'de'
    PROPERTY_HOUSE = 'ca'
    PROPERTY_OFFICE = 'of'
    PROPERTY_SHOP = 'lc'
    PROPERTY_URBAN_SITE = 'su'
    PROPERTY_PARCEL = 'pa'
    PROPERTY_INDUSTRIAL = 'in'
    PROPERTY_CELLAR = 'bo'
    PROPERTY_PARKING = 'es'
    PROPERTY_VACATION = 'va'


    PROPERTY_CHOICES = (
        (PROPERTY_APARTMENT, 'Departamento'),
        (PROPERTY_HOUSE, 'Casa'),
        (PROPERTY_OFFICE, 'Oficina'),
        (PROPERTY_SHOP, 'Local Comercial'),
        (PROPERTY_URBAN_SITE, 'Sitio Urbano'),
        (PROPERTY_PARCEL, 'Parcela'),
        (PROPERTY_INDUSTRIAL, 'Industrial'),
        (PROPERTY_CELLAR, 'Bodega'),
        (PROPERTY_PARKING, 'Estacionamiento'),
        (PROPERTY_VACATION, 'Vacacional'),
    )

    PUBLISH_BUY = 've'
    PUBLISH_RENT = 'ar'
    PUBLISH_RENTAL_SEASON = 'at'

    PUBLISH_CHOICES = (
        (PUBLISH_BUY, 'Venta'),
        (PUBLISH_RENT, 'Arriendo'),
        (PUBLISH_RENTAL_SEASON, 'Arriendo Temporada'),
    )

    TYPE_PRICE_CHOICES = (
         ('uf', 'UF'),
         ('clp', '$'),
    )

    # General
    property_type = models.CharField('Tipo de Propiedad*', choices=PROPERTY_CHOICES, max_length=2)
    publish_type = models.CharField('Tipo de Operación*', choices=PUBLISH_CHOICES, max_length=2)
    land_surface = models.PositiveIntegerField("Superficie terreno (m²)*")
    title = models.CharField("Titulo*", max_length=150)
    description = models.TextField("Descripción*")
    type_price = models.CharField('Tipo Precio*', choices=TYPE_PRICE_CHOICES, max_length=3)
    price = models.PositiveIntegerField('Precio*')

    #miniatura
    thumbnail = models.ImageField('Imagen (Opcional)',upload_to=property_directory_path, blank=True)

    # locacion
    # region = models.CharField("Region*", max_length=50, blank=True)
    # commune = models.CharField("Comuna*", max_length=50, blank=True)
    region = models.ForeignKey('Region', on_delete=models.CASCADE, verbose_name='Región*')
    commune = models.ForeignKey('Commune', on_delete=models.CASCADE, verbose_name='Comuna*')
    street_address = models.CharField("Calle*", max_length=50)
    street_number = models.CharField("Número*", max_length=50)

    # contact
    phone1 = models.CharField('Telefono 1 (Opcional)', max_length=9, blank=True)
    phone2 = models.CharField('Telefono 2 (Opcional)', max_length=9, blank=True)

    # extras for urls
    slug = models.SlugField(null=False, unique=True, blank=True)
    location_slug = models.SlugField(null=False, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    

    class Meta:
        '''Meta definition for Property.'''

        verbose_name = 'Property'
        verbose_name_plural = 'Properties'

    def __str__(self):
        return f"{self.get_property_type_display()} - {self.title}"

    def get_absolute_url(self):
        return reverse("property_detail", kwargs={"publish_type": self.publish_type, "property_type": self.property_type, 'location_slug': self.location_slug,"slug": self.slug, 'uuid': self.uuid})

class PropertyImage(TimeStampedModel):
    '''Model definition for PropertyImage.'''
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='properties')
    image = models.ImageField(upload_to=property_images_directory_path)

    class Meta:
        '''Meta definition for PropertyImage.'''

        verbose_name = 'PropertyImage'
        verbose_name_plural = 'PropertyImages'

    def __str__(self):
        return self.property.title

class House(TimeStampedModel):
    '''Model definition for House.'''
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='houses', blank=True, null=True)
    builded_surface = models.PositiveIntegerField("Superficie construida (m²)*")
    num_rooms = models.PositiveBigIntegerField('Dormitorios*')
    num_bathrooms = models.PositiveIntegerField('Baños*')
    floor_type = models.CharField("Tipo piso*", max_length=150)
    is_furnished = models.BooleanField("Esta propiedad está amoblada*", default=False)
    num_parkings = models.PositiveIntegerField('Estacionamientos (Opcional)', blank=True, null=True)
    num_cellars = models.PositiveIntegerField('Bodegas (Opcional)', blank=True, null=True)
    num_floors = models.PositiveIntegerField('Pisos (Opcional)', blank=True, null=True)
    num_house = models.CharField("Número casa (Opcional)", max_length=20, blank=True, null=True)
    builded_year = models.PositiveIntegerField('Año de Construcción (Opcional)', blank=True, null=True)
    class Meta:
        '''Meta definition for House.'''

        ordering = ('-created',)
        verbose_name = 'House'
        verbose_name_plural = 'Houses'

    def __str__(self):
        return self.property.title

class Apartment(TimeStampedModel):
    '''Model definition for House.'''
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='apartments', blank=True, null=True)
    builded_surface = models.PositiveIntegerField("Superficie construida (m²)*")
    num_rooms = models.PositiveBigIntegerField('Dormitorios*')
    num_bathrooms = models.PositiveIntegerField('Baños*')
    floor_type = models.CharField("Tipo piso*", max_length=150)
    is_furnished = models.BooleanField("Esta propiedad está amoblada*", default=False)
    num_parkings = models.PositiveIntegerField('Estacionamientos (Opcional)', blank=True, null=True)
    num_cellars = models.PositiveIntegerField('Bodegas (Opcional)', blank=True, null=True)
    num_floors = models.PositiveIntegerField('Pisos (Opcional)', blank=True, null=True)
    num_apartment = models.CharField("Número depto (Opcional)", max_length=20, blank=True, null=True)
    builded_year = models.PositiveIntegerField('Año de Construcción (Opcional)', blank=True, null=True)
    common_expenses = models.PositiveIntegerField('Gastos comunes*')
    class Meta:
        '''Meta definition for House.'''

        ordering = ('-created',)
        verbose_name = 'Apartment'
        verbose_name_plural = 'Apartments'

    def __str__(self):
        return self.property.title

class Region(TimeStampedModel):

    # REGION_METROPOLITANA = 'met'
    # REGION_ANTOFAGASTA = 'an'
    # REGION_ARAUCANIA = 'ar'
    # REGION_ARICA_Y_PARINATOCA = 'ap'
    # REGION_ATACAMA = 'at'
    # REGION_AYSEN = 'ay'
    # REGION_BERNARDO_OHIGGINS = 'bo'
    # REGION_BIOBIO = 'bb'
    # REGION_COQUIMBO = 'co'
    # REGION_LOS_LAGOS = 'll'
    # REGION_LOS_RIOS = 'lr'
    # REGION_MAGALLANES = 'mag'
    # REGION_MAULE = 'mau'
    # REGION_NUBLE = 'nb'
    # REGION_TARAPACA = 'ta'
    # REGION_VALPARAISO = 'va'

    # REGION_CHOICES = (
    #     (REGION_METROPOLITANA, 'Metropolitana'),
    #     (REGION_ANTOFAGASTA, 'Antofagasta'),
    #     (REGION_ARAUCANIA, 'Araucania'),
    #     (REGION_ARICA_Y_PARINATOCA, 'Arica y Parinatoca'),
    #     (REGION_ATACAMA, 'Atacama'),
    #     (REGION_AYSEN, 'Aysen'),
    #     (REGION_BERNARDO_OHIGGINS, 'Bernardo Ohiggins'),
    #     (REGION_BIOBIO, 'Biobío'),
    #     (REGION_COQUIMBO, 'Coquimbo'),
    #     (REGION_LOS_LAGOS, 'Los Lagos'),
    #     (REGION_LOS_RIOS, 'Los Rios'),
    #     (REGION_MAGALLANES, 'Magallanes'),
    #     (REGION_MAULE, 'Maule'),
    #     (REGION_NUBLE, 'Ñuble'),
    #     (REGION_TARAPACA, 'Tarapaca'),
    #     (REGION_VALPARAISO, 'Valparaiso'),
    # )

    # class Regions(models.TextChoices):
    #     REGION_METROPOLITANA = 'met', 'Metropolitana'
    #     REGION_ANTOFAGASTA = 'an', 'Antofagasta'
    #     REGION_ARAUCANIA = 'ar', 'Araucania'
    #     REGION_ARICA_Y_PARINATOCA = 'ap', 'Arica y Parinatoca'
    #     REGION_ATACAMA = 'at', 'Atacama'
    #     REGION_AYSEN = 'ay', 'Aysen'
    #     REGION_BERNARDO_OHIGGINS = 'bo', 'Bernardo Ohiggins'
    #     REGION_BIOBIO = 'bb', 'Biobío'
    #     REGION_COQUIMBO = 'co', 'Coquimbo'
    #     REGION_LOS_LAGOS = 'll', 'Los Lagos'
    #     REGION_LOS_RIOS = 'lr', 'Los Rios'
    #     REGION_MAGALLANES = 'mag', 'Magallanes'
    #     REGION_MAULE = 'mau', 'Maule'
    #     REGION_NUBLE = 'nb', 'Ñuble'
    #     REGION_TARAPACA = 'ta', 'Tarapaca'
    #     REGION_VALPARAISO = 'va', 'Valparaiso'


    '''Model definition for Region.'''
    name = models.CharField('Comuna', max_length=150)

    class Meta:
        '''Meta definition for Region.'''

        verbose_name = 'Region'
        verbose_name_plural = 'Regions'

    def __str__(self):
        return self.name

class Commune(TimeStampedModel):
    '''Model definition for Commune.'''
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='communes')
    name = models.CharField('Comuna', max_length=150)
    class Meta:
        '''Meta definition for Commune.'''

        verbose_name = 'Commune'
        verbose_name_plural = 'Communes'

    def __str__(self):
        return self.name


# def property_save(sender, instance, **kwargs):

    # estacionamiento = Estacionamiento.objects.filter(
    #     id=instance.estacionamiento_id)
    # if instance.estado_plan == "iniciado":
    #     estacionamiento.update(estado_estacionamiento="reservado")
    # if instance.estado_plan == "terminado":
        # estacionamiento.update(estado_estacionamiento="disponible")


# post_save.connect(property_save, sender=Property)
