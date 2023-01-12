from django.db.models.signals import post_save

from .utils import send_property_email
from .models import PropertyContact, Property, PropertyManager


def contact_post_save(sender, instance, created, **kwargs):
    if created:
        send_property_email(instance.property.get_absolute_url(), instance.name, instance.phone, instance.property, instance.message, instance.from_email)
        
post_save.connect(contact_post_save, PropertyContact)

def property_post_save(sender, instance, created, **kwargs):
    if instance.status != 'pu' and instance.status != 'dr':

        iva = ''
        if instance.is_iva == True:
            iva = 'con IVA'
        else:
            iva = 'sin IVA'
            
        PropertyManager.objects.create(
            property=instance,
            type_property=f'{instance.get_property_type_display()} {instance.get_publish_type_display()}',
            total='{0} {1} {2}'.format(instance.price, instance.get_type_price_display(), iva),
            commission_percentage=instance.commission_percentage,
            commission_value=instance.commission_value
        )
        
post_save.connect(property_post_save, Property)