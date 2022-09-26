from django.db import models

from apps.base.models import TimeStampedModel
# Create your models here.

class Contact(TimeStampedModel):
    """Model definition for Contact."""

    # TODO: Define fields here
    name = models.CharField('Nombre Completo', max_length=200)
    from_email = models.EmailField('Email', max_length=50)
    subject = models.CharField('Asunto', max_length=50)
    phone = models.CharField('Télefono(opcional)', max_length=9, blank=True)
    message = models.TextField('Mensaje')

    class Meta:
        """Meta definition for Contact."""

        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        """Unicode representation of Contact."""
        return self.name