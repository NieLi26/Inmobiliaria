import uuid 
from django.db import models
from core.settings import MEDIA_URL, STATIC_URL
from django.urls import reverse


from apps.base.models import BaseModel

# Create your models here.

def house_directory_path(instance,filename):
    return 'houses/{0}/{1}'.format(instance.location.street_address, filename)

def house_images_directory_path(instance,filename):
    return 'house_images/{0}/{1}'.format(instance.house.location.street_address, filename)

def apartment_directory_path(instance,filename):
    return 'houses/{0}/{1}'.format(instance.location.street_address, filename)

def apartment_images_directory_path(instance,filename):
    return 'house_images/{0}/{1}'.format(instance.apartment.location.street_address, filename)



class Location(BaseModel):

    PROPERTY_APARTMENT = 'de'
    PROPERTY_HOUSE = 'ca'
    PROPERTY_OFFICE = 'of'
    PROPERTY_SHOP = 'lc'
    PROPERTY_LAND = 'te'
    PROPERTY_PARCEL = 'pa'
    PROPERTY_FARMING = 'ag'
    PROPERTY_INDUSTRIAL = 'in'
    PROPERTY_CELLAR = 'bo'
    PROPERTY_PARKING = 'es'
    PROPERTY_VACATION = 'va'


    PROPERTY_CHOICES = (
        (PROPERTY_APARTMENT, 'Departamento'),
        (PROPERTY_HOUSE, 'Casa'),
        (PROPERTY_OFFICE, 'Oficina'),
        (PROPERTY_SHOP, 'Local Comercial'),
        (PROPERTY_LAND, 'Terreno'),
        (PROPERTY_PARCEL, 'Parcela'),
        (PROPERTY_FARMING, 'Agrícola'),
        (PROPERTY_INDUSTRIAL, 'Industrial'),
        (PROPERTY_CELLAR, 'Bodega'),
        (PROPERTY_PARKING, 'Estacionamiento'),
        (PROPERTY_VACATION, 'Vacacional'),
    )

    property_type = models.CharField('Tipo de Propiedad', choices=PROPERTY_CHOICES, max_length=2)
    region = models.CharField("Region", max_length=50)
    commune = models.CharField("Comuna", max_length=50)
    street_address = models.CharField("Calle", max_length=50)
    street_number = models.CharField("Número", max_length=50)
    house_number = models.CharField("Número depto/casa (Opcional)", max_length=50, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return self.street_address

    def get_absolute_url(self):
        return reverse("location_detail", kwargs={"pk": self.pk})

class House(BaseModel):

    PUBLISH_BUY = 've'
    PUBLISH_RENT = 'ar'
    PUBLISH_RENTAL_SEASON = 'at'

    PUBLISH_CHOICES = (
        (PUBLISH_BUY, 'Venta'),
        (PUBLISH_RENT, 'Arriendo'),
        (PUBLISH_RENTAL_SEASON, 'Arriendo Temporada'),
    )

    
    SUB_PROPERTY_HOUSE = 'ca'
    SUB_PROPERTY_ROOM = 'pi'
    SUB_PROPERTY_HOUSING_COMPLEX = 'ch'
    SUB_PROPERTY_CONDOMINIUM = 'co'
    SUB_PROPERTY_BUNGALOW = 'bu'

    
    SUB_PROPERTY_CHOICES = (
        (SUB_PROPERTY_HOUSE, 'Casa'),
        (SUB_PROPERTY_ROOM, 'Pieza'),
        (SUB_PROPERTY_HOUSING_COMPLEX, 'Conjunto Habitacional'),
        (SUB_PROPERTY_CONDOMINIUM, 'Condominio'),
        (SUB_PROPERTY_BUNGALOW, 'Bungalow'),

    )

    SUB_RENT_MONTHLY = 'am'
    SUB_RENT_WEEKLY = 'as'
    SUB_RENT_DAILY = 'ad'

    SUB_RENT_CHOICES = (
        (SUB_RENT_MONTHLY, 'Arriendo Mensual'),
        (SUB_RENT_WEEKLY, 'Arriendo Semanal'),
        (SUB_RENT_DAILY, 'Arriendo Diario'),
    )


    NUM_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )

    
    TYPE_PRICE_CHOICES = (
         ('uf', 'UF'),
         ('clp', '$'),
    )

    ORIENTATION_N = 'n'
    ORIENTATION_S = 's'
    ORIENTATION_E = 'o'
    ORIENTATION_W = 'p'
    ORIENTATION_N_S = 'ns'
    ORIENTATION_N_E = 'no'
    ORIENTATION_N_W = 'np'
    ORIENTATION_S_E = 'so'
    ORIENTATION_S_W = 'sp'
    ORIENTATION_E_W = 'op'
    ORIENTATION_N_S_E = 'nso'
    ORIENTATION_N_S_W = 'nsp'
    ORIENTATION_N_E_W = 'nop'
    ORIENTATION_S_E_W = 'sop'
    ORIENTATION_ALL = 'all'

    ORIENTATION_CHOICES = (
        (ORIENTATION_N, 'Norte'),
        (ORIENTATION_S, 'Sur'),
        (ORIENTATION_E, 'Oriente'),
        (ORIENTATION_W, 'Poniente'),
        (ORIENTATION_N_S, 'Norte - Sur'),
        (ORIENTATION_N_E, 'Nor - Oriente'),
        (ORIENTATION_N_W, 'Nor - Poniente'),
        (ORIENTATION_S_E, 'Sur - Oriente'),
        (ORIENTATION_S_W, 'Sur - Poniente'),
        (ORIENTATION_E_W, 'Oriente - Poniente'),
        (ORIENTATION_N_S_E, 'Norte - Sur - Oriente'),
        (ORIENTATION_N_S_W, 'Norte - Sur - Poniente'),
        (ORIENTATION_N_E_W, 'Norte - Oriente - Poniente'),
        (ORIENTATION_S_E_W, 'Sur - Oriente - Poniente'),
        (ORIENTATION_ALL, 'Todas'),
    )

    SERVICE_CHOICES = (
        ('s', 'Si'),
        ('n', 'No'),
    )


    location = models.ForeignKey(Location, verbose_name="Locación", on_delete=models.CASCADE, related_name='houses')
    title = models.CharField("Titulo", max_length=150)
    slug = models.CharField("Slug", max_length=250, blank=True)
    sub_property_type = models.CharField("Subtipo de propiedad", choices=SUB_PROPERTY_CHOICES , max_length=2)
    builded_surface = models.PositiveIntegerField("Superficie construida (m²)")
    land_surface = models.PositiveIntegerField("Superficie terreno (m²)")
    num_rooms = models.CharField('Dormitorios', choices=NUM_CHOICES, max_length=2)
    num_bathrooms = models.CharField('Baños', choices=NUM_CHOICES, max_length=2)
    floor_type = models.CharField("Tipo piso", max_length=150)
    description = models.TextField("Descripción")
    is_furnished = models.BooleanField("Esta propiedad está amoblada", default=False)
    sub_rent_type = models.CharField("Subtipo de renta", choices=SUB_RENT_CHOICES , max_length=2, blank=True)
    thumbnail = models.ImageField('Imagen',upload_to=house_directory_path, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Opcional
    service = models.CharField('Servicio', choices=SERVICE_CHOICES, max_length=1, blank=True)
    num_parkings = models.CharField('Estacionamientos', choices=NUM_CHOICES, max_length=2, blank=True)
    num_cellars = models.CharField('Bodegas', choices=NUM_CHOICES, max_length=2, blank=True)
    num_floors = models.PositiveIntegerField('Pisos', blank=True, null=True)
    builded_year = models.PositiveIntegerField('Año de Construcción', blank=True, null=True)
    orientation = models.CharField("Orientación", choices=ORIENTATION_CHOICES , max_length=3, blank=True)

    publish_type = models.CharField('Tipo de Operación', choices=PUBLISH_CHOICES, max_length=2)
    type_price = models.CharField('Tipo Precio', choices=TYPE_PRICE_CHOICES, max_length=3)
    price = models.PositiveIntegerField('Precio')


    class Meta:
        verbose_name = "House"
        verbose_name_plural = "Houses"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return reverse("house_detail", kwargs={"uuid": self.uuid})
        return reverse("house_detail", args=[str(self.uuid)])

class HouseImage(BaseModel):
    """Model definition for PropertyImage."""

    # TODO: Define fields here
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='houses')
    image = models.ImageField(upload_to=house_images_directory_path)

    class Meta:
        """Meta definition for PropertyImage."""

        verbose_name = 'HouseImage'
        verbose_name_plural = 'HouseImages'

    def __str__(self):
        """Unicode representation of HouseImage."""
        return self.house.title

class Apartment(BaseModel):

    PUBLISH_BUY = 've'
    PUBLISH_RENT = 'ar'
    PUBLISH_RENTAL_SEASON = 'at'

    PUBLISH_CHOICES = (
        (PUBLISH_BUY, 'Venta'),
        (PUBLISH_RENT, 'Arriendo'),
        (PUBLISH_RENTAL_SEASON, 'Arriendo Temporada'),
    )

    
    SUB_PROPERTY_APARTMENT = 'de'
    SUB_PROPERTY_LOFT = 'lo'
    SUB_PROPERTY_DUPLEX = 'du'
    SUB_PROPERTY_CONDOMINIUM = 'co'

    
    SUB_PROPERTY_CHOICES = (
        (SUB_PROPERTY_APARTMENT, 'Departamento'),
        (SUB_PROPERTY_LOFT, 'Loft'),
        (SUB_PROPERTY_DUPLEX, 'Dúplex'),
        (SUB_PROPERTY_CONDOMINIUM, 'Condominio'),

    )

    SUB_RENT_MONTHLY = 'am'
    SUB_RENT_WEEKLY = 'as'
    SUB_RENT_DAILY = 'ad'

    SUB_RENT_CHOICES = (
        (SUB_RENT_MONTHLY, 'Arriendo Mensual'),
        (SUB_RENT_WEEKLY, 'Arriendo Semanal'),
        (SUB_RENT_DAILY, 'Arriendo Diario'),
    )


    NUM_ROOMS_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )

    NUM_BATHROOMS_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )
    
    TYPE_PRICE_CHOICES = (
         ('uf', 'UF'),
         ('clp', '$'),
    )


    location = models.ForeignKey(Location, verbose_name="Locación", on_delete=models.CASCADE, related_name='apartments')
    title = models.SlugField("Titulo", max_length=150)
    sub_property_type = models.CharField("Subtipo de propiedad", choices=SUB_PROPERTY_CHOICES , max_length=2)
    builded_surface = models.PositiveIntegerField("Superficie construida (m²)")
    land_surface = models.PositiveIntegerField("Superficie terreno (m²)")
    num_rooms = models.CharField('Dormitorios', choices=NUM_ROOMS_CHOICES, max_length=2)
    num_bathrooms = models.CharField('Baños', choices=NUM_BATHROOMS_CHOICES, max_length=2)
    common_expenses = models.PositiveIntegerField('Gasos comunes')
    floor_type = models.CharField("Tipo piso", max_length=150)
    description = models.TextField("Descripción")
    is_furnished = models.BooleanField("Esta propiedad está amoblada", default=False)
    sub_rent_type = models.CharField("Subtipo de renta", choices=SUB_RENT_CHOICES , max_length=2, blank=True)
    thumbnail = models.ImageField('Imagen',upload_to=apartment_directory_path, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    publish_type = models.CharField('Tipo de Operación', choices=PUBLISH_CHOICES, max_length=2)
    type_price = models.CharField('Tipo Precio', choices=TYPE_PRICE_CHOICES, max_length=3)
    price = models.PositiveIntegerField('Precio')


    class Meta:
        verbose_name = "Apartment"
        verbose_name_plural = "Apartments"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("apartment_detail", kwargs={"uuid": self.uuid})


class ApartmentImage(BaseModel):
    """Model definition for PropertyImage."""

    # TODO: Define fields here
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='apartments')
    image = models.ImageField(upload_to=apartment_images_directory_path)

    class Meta:
        """Meta definition for PropertyImage."""

        verbose_name = 'ApartmentImage'
        verbose_name_plural = 'ApartmentImages'

    def __str__(self):
        """Unicode representation of HouseImage."""
        return self.apartment.title