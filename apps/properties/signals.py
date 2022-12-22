from django.db.models.signals import post_save

from .utils import send_property_email
from .models import PropertyContact


def contact_post_save(sender, instance, created, **kwargs):
    if created:
        send_property_email(instance.property.get_absolute_url(), instance.name, instance.phone, instance.property, instance.message, instance.from_email)
        
post_save.connect(contact_post_save, PropertyContact)