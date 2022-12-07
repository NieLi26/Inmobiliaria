from django.forms import model_to_dict
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

    # url externas
    google_url = models.TextField('Google Maps', blank=True, null=True)
    video_url = models.URLField('Video', blank=True, null=True)

    is_featured = models.BooleanField('Destacada?', default=False)

    #miniatura
    thumbnail = models.ImageField('Imagen (Opcional)',upload_to=property_directory_path, blank=True)

    # locacion
    region = models.ForeignKey('Region', on_delete=models.CASCADE, verbose_name='Región*', related_name='properties')
    commune = models.ForeignKey('Commune', on_delete=models.CASCADE, verbose_name='Comuna*', related_name='properties')
    street_address = models.CharField("Calle*", max_length=50)
    street_number = models.CharField("Número*", max_length=50)
    # google api for location
    longitude = models.CharField("Longitud", max_length=250, blank=True)
    latitude = models.CharField("Latitud", max_length=250, blank=True)

    # contact
    phone1 = models.CharField('Telefono 1 (Opcional)', max_length=9, blank=True)
    phone2 = models.CharField('Telefono 2 (Opcional)', max_length=9, blank=True)

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


# def property_save(sender, instance, **kwargs):

    # estacionamiento = Estacionamiento.objects.filter(
    #     id=instance.estacionamiento_id)
    # if instance.estado_plan == "iniciado":
    #     estacionamiento.update(estado_estacionamiento="reservado")
    # if instance.estado_plan == "terminado":
        # estacionamiento.update(estado_estacionamiento="disponible")


# post_save.connect(property_save, sender=Property)



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