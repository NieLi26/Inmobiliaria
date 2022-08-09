from django import	template

from apps.pages.models import Contact

# para registrar etiqueta de plantilla
register = template.Library()

@register.simple_tag
def contact_state_count():
    qs = Contact.objects.filter(state=True)
    if qs.exists():
        return qs.count()
    return 0

