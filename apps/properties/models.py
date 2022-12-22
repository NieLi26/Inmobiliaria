import os
from django.forms import model_to_dict
import uuid 
from django.db import models
from core.settings import MEDIA_URL, STATIC_URL
from django.urls import reverse
# from django.db.models.signals import post_save

# multi select
from multiselectfield import MultiSelectField

from apps.base.models import TimeStampedModel

def property_directory_path(instance,filename):
    return 'property/{0}/{1}'.format(instance.uuid, filename)

def property_images_directory_path(instance,filename):
    return 'property_images/{0}/{1}'.format(instance.property.uuid, filename)

class Realtor(TimeStampedModel):
    '''Model definition for Realtor.'''
    first_name = models.CharField('Nombre', max_length=200)
    last_name = models.CharField('Apellido', max_length=200)
    phone1 = models.CharField('Telefono 1', max_length=9)
    phone2 = models.CharField('Telefono 2', max_length=9, blank=True)
    email = models.EmailField('Correo', max_length=150)
    class Meta:
        '''Meta definition for Realtor.'''

        verbose_name = 'Realtor'
        verbose_name_plural = 'Realtors'

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('properties:realtor_detail', kwargs={'pk': self.pk})

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
    PUBLISH_EXCHANGE = 'pe'

    PUBLISH_CHOICES = (
        ('', 'Seleccione un tipo'),
        (PUBLISH_BUY, 'Venta'),
        (PUBLISH_RENT, 'Arriendo'),
        (PUBLISH_RENTAL_SEASON, 'Arriendo Temporada'),
        (PUBLISH_EXCHANGE, 'Permuta')
    )

    TYPE_PRICE_CHOICES = (
        ('', 'Seleccione un tipo'),
         ('uf', 'UF'),
         ('usd', 'USD'),
         ('clp', 'CLP'),
    )

    # General
    realtor = models.ForeignKey(Realtor, on_delete=models.CASCADE, related_name='properties')
    property_type = models.CharField('Tipo de Propiedad', choices=PROPERTY_CHOICES, max_length=2)
    publish_type = models.CharField('Tipo de Operación', choices=PUBLISH_CHOICES, max_length=2)
    land_surface = models.PositiveIntegerField("Superficie terreno (m²)", default=0)
    title = models.CharField("Titulo(hasta 100 caracteres)", max_length=100)
    description = models.TextField("Descripción")
    type_price = models.CharField('Tipo Moneda', choices=TYPE_PRICE_CHOICES, max_length=3)
    price = models.PositiveIntegerField('Precio', default=0)

    # url externas
    google_url = models.TextField('Ubicación en Google Maps', blank=True, null=True)
    video_url = models.URLField('Video', blank=True, null=True)

    # status
    is_featured = models.BooleanField('Destacada?', default=False)
    is_new = models.BooleanField('Nueva?', default=False)

    # miniatura
    thumbnail = models.ImageField('Imagen',upload_to=property_directory_path, blank=True)

    # locacion
    region = models.ForeignKey('Region', on_delete=models.CASCADE, verbose_name='Región', related_name='properties')
    commune = models.ForeignKey('Commune', on_delete=models.CASCADE, verbose_name='Comuna', related_name='properties')
    street_address = models.CharField("Calle", max_length=50)
    street_number = models.PositiveIntegerField("Número")

    # google api for location
    longitude = models.CharField("Longitud", max_length=250, blank=True)
    latitude = models.CharField("Latitud", max_length=250, blank=True)

    # extras for urls
    slug = models.SlugField(null=False, unique=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    

    class Meta:
        '''Meta definition for Property.'''

        verbose_name = 'Property'
        verbose_name_plural = 'Properties'

    def __str__(self):
        return f"{self.get_property_type_display()} - {self.title}"

    def toJSON(self):
        item = model_to_dict(self)
        return item

    def get_absolute_url(self):
        return reverse("properties:property_detail", kwargs={"publish_type": self.publish_type, "property_type": self.property_type, 'location_slug': self.commune.location_slug,"slug": self.slug, 'uuid': self.uuid})

class PropertyImage(TimeStampedModel):
    '''Model definition for PropertyImage.'''
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='properties')
    image = models.ImageField(upload_to=property_images_directory_path)

    class Meta:
        '''Meta definition for PropertyImage.'''

        verbose_name = 'PropertyImage'
        verbose_name_plural = 'PropertyImages'

    # def delete(self):
    #     # opcion 1
    #     image = self.image.path
    #     if os.path.isfile(image):
    #         os.remove(image)
    #     #opcion 2
    #     self.image.delete()
    #     return super().delete()

    def __str__(self):
        return self.property.title

    def get_image(self):
        if self.image:
            return "{}{}".format(MEDIA_URL, self.image)
        return "{}{}".format(STATIC_URL, "img/empty.png")
    
    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

class House(TimeStampedModel):

    class Others(models.TextChoices):
        BLINDS = 'Persianas', 'Persianas'
        WINDOW_PROTECTIONS = 'Protecciones Ventana', 'Protecciones Ventana'
        THERMOPANELS = 'Termopaneles', 'Termopaneles'

    class Distributions(models.TextChoices):
        BATHROOM_VISIT= 'Baño Visita', 'Baño Visita'
        HALL = 'Hall', 'Hall'
        GARDEN_SUEDE = 'Antejardin', 'Antejardin'
        SERVICE_YARD = 'Patio de Servicio', 'Patio de Servicio'
        SERVICE_ROOM = 'Estar de Servicio', 'Estar de Servicio'
        GARDEN = 'Jardin', 'Jardin'
        PANTRY = 'Despensa', 'Despensa'
        LIVING_ROOM = 'Sala Estar', 'Sala Estar'
        QUNCHO = 'Quincho', 'Quincho'
        INDOOR_LAUNDRY = 'Lavadero Interior', 'Lavadero Interior'
        OUTDOOR_LAUNDRY = 'Lavadero Exterior', 'Lavadero Exterior'
        DESK = 'Escritorio', 'Escritorio'
        MANSARD = 'Mansarda', 'Mansarda'
        TERRACE = 'Terraza', 'Terraza'

    class Services(models.TextChoices):
        ALARM = 'Alarma', 'Alarma'
        JACUZZI = 'Jacuzzi', 'Jacuzzi'
        PHONE = 'Telefono', 'Telefono'
        AUTOMATIC_IRRIGATION = 'Riego Automatico', 'Riego Automatico'
        AUTOMATIC_DOOR = 'Porton Automatico', 'Porton Automatico'
        SWIMMING_POOL = 'Piscina', 'Piscina'
        TV = 'TV Cable', 'TV Cable'
        CHIMNEY = 'Chimenea', 'Chimenea'
        HEATING = 'Calefaccion', 'Calefaccion'
        AIR_CONDITIONING = 'Aire Acondicionado', 'Aire Acondicionado'
        
    class Kitchens(models.TextChoices):
        DAILY_DINING_ROOM = 'Comedor Diario', 'Comedor Diario'
        EQUIPPED_KITCHEN  = 'Cocina Equipada', 'Cocina Equipada'
        FURNISHED_KITCHEN = 'Cocina Amoblada', 'Cocina Amoblada'


    '''Model definition for House.'''
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='houses', blank=True, null=True)
    builded_surface = models.PositiveIntegerField("Superficie construida (m²)", default=0)
    num_rooms = models.PositiveIntegerField('Dormitorios', default=0)
    num_bathrooms = models.PositiveIntegerField('Baños', default=0)
    num_parkings = models.PositiveIntegerField('Estacionamientos', blank=True, null=True, default=0)
    num_cellars = models.PositiveIntegerField('Bodegas', blank=True, null=True, default=0)
    num_floors = models.PositiveIntegerField('Pisos', blank=True, null=True, default=0)
    num_house = models.PositiveIntegerField("Número Casa", blank=True, null=True)
    builded_year = models.PositiveIntegerField('Año de Construcción', blank=True, null=True, default=0)
    common_expenses = models.PositiveIntegerField('Gastos comunes', default=0)
    # Distribución
    distribution = MultiSelectField('Distribución', choices=Distributions.choices, max_length=250, default="")
    # # Servicios
    service = MultiSelectField('Servicios', choices=Services.choices, max_length=250, default="")
    # # cocina
    kitchen = MultiSelectField('Cocina',choices=Kitchens.choices , max_length=250, default="")
    # # otros
    other = MultiSelectField('Otros',choices=Others.choices , max_length=250, default="")




    class Meta:
        '''Meta definition for House.'''

        ordering = ('-created',)
        verbose_name = 'House'
        verbose_name_plural = 'Houses'

    def __str__(self):
        return self.property.title

class Apartment(TimeStampedModel):

    class Others(models.TextChoices):
        BLINDS = 'Persianas', 'Persianas'
        WINDOW_PROTECTIONS = 'Protecciones Ventana', 'Protecciones Ventana'
        THERMOPANELS = 'Termopaneles', 'Termopaneles'

    class Distributions(models.TextChoices):
        BATHROOM_VISIT= 'Baño Visita', 'Baño Visita'
        HALL = 'Hall', 'Hall'
        GARDEN_SUEDE = 'Antejardin', 'Antejardin'
        SERVICE_YARD = 'Patio de Servicio', 'Patio de Servicio'
        SERVICE_ROOM = 'Estar de Servicio', 'Estar de Servicio'
        GARDEN = 'Jardin', 'Jardin'
        PANTRY = 'Despensa', 'Despensa'
        LIVING_ROOM = 'Sala Estar', 'Sala Estar'
        QUNCHO = 'Quincho', 'Quincho'
        INDOOR_LAUNDRY = 'Lavadero Interior', 'Lavadero Interior'
        OUTDOOR_LAUNDRY = 'Lavadero Exterior', 'Lavadero Exterior'
        DESK = 'Escritorio', 'Escritorio'
        MANSARD = 'Mansarda', 'Mansarda'
        TERRACE = 'Terraza', 'Terraza'

    class Services(models.TextChoices):
        ALARM = 'Alarma', 'Alarma'
        JACUZZI = 'Jacuzzi', 'Jacuzzi'
        PHONE = 'Telefono', 'Telefono'
        AUTOMATIC_IRRIGATION = 'Riego Automatico', 'Riego Automatico'
        AUTOMATIC_DOOR = 'Porton Automatico', 'Porton Automatico'
        SWIMMING_POOL = 'Piscina', 'Piscina'
        TV = 'TV Cable', 'TV Cable'
        CHIMNEY = 'Chimenea', 'Chimenea'
        HEATING = 'Calefaccion', 'Calefaccion'
        AIR_CONDITIONING = 'Aire Acondicionado', 'Aire Acondicionado'
        
    class Kitchens(models.TextChoices):
        DAILY_DINING_ROOM = 'Comedor Diario', 'Comedor Diario'
        EQUIPPED_KITCHEN  = 'Cocina Equipada', 'Cocina Equipada'
        FURNISHED_KITCHEN = 'Cocina Amoblada', 'Cocina Amoblada'

    '''Model definition for House.'''
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='apartments', blank=True, null=True)
    builded_surface = models.PositiveIntegerField("Superficie construida (m²)", default=0)
    num_rooms = models.PositiveIntegerField('Dormitorios', default=0)
    num_bathrooms = models.PositiveIntegerField('Baños', default=0)
    num_parkings = models.PositiveIntegerField('Estacionamientos', blank=True, null=True, default=0)
    num_cellars = models.PositiveIntegerField('Bodegas', blank=True, null=True, default=0)
    num_floors = models.PositiveIntegerField('Pisos', blank=True, null=True, default=0)
    num_apartment = models.PositiveIntegerField("Número Depto", blank=True, null=True)
    builded_year = models.PositiveIntegerField('Año de Construcción', blank=True, null=True, default=0)
    common_expenses = models.PositiveIntegerField('Gastos comunes', default=0)

    distribution = MultiSelectField('Distribución', choices=Distributions.choices, max_length=250, default="")
    service = MultiSelectField('Servicios', choices=Services.choices, max_length=250, default="")
    kitchen = MultiSelectField('Cocina',choices=Kitchens.choices , max_length=250, default="")
    other = MultiSelectField('Otros',choices=Others.choices , max_length=250, default="")


    class Meta:
        '''Meta definition for House.'''

        ordering = ('-created',)
        verbose_name = 'Apartment'
        verbose_name_plural = 'Apartments'

    def __str__(self):
        return self.property.title

class Region(TimeStampedModel):

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
    location_slug = models.SlugField()
    class Meta:
        '''Meta definition for Commune.'''

        verbose_name = 'Commune'
        verbose_name_plural = 'Communes'

    def __str__(self):
        return self.name

    def get_commune_region(self):
        return f"{self.name}, {self.region}"

class PropertyContact(TimeStampedModel):
    '''Model definition for PropertyContact.'''
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_contacts')
    name = models.CharField('Nombre Completo', max_length=200)
    from_email = models.EmailField('Email', max_length=50)
    phone = models.CharField('Télefono(opcional)', max_length=9, blank=True)
    message = models.TextField('Mensaje')
    class Meta:
        '''Meta definition for PropertyContact.'''

        verbose_name = 'PropertyContact'
        verbose_name_plural = 'PropertyContacts'

    def __str__(self):
        return str(self.from_email)

