from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

from .models import Property, Commune


def url_custom_list(publish_type, property_type, location_slug, page_number=None): 
    property_choices = Property.PROPERTY_CHOICES
    list_property_type = [i[0] for i in property_choices]
    list_location_slug = [i.location_slug for i in Commune.objects.all()]

    try:

        if (publish_type != 've' and publish_type != 'ar' and publish_type != 'at') and property_type in list_property_type and location_slug in list_location_slug:
            print('entrre en propiedad - locacion')
            return reverse('properties:custom_list_publish_property', args=[property_type, location_slug])
        elif (publish_type == 've' or publish_type == 'ar' or publish_type == 'at') and property_type not in list_property_type and location_slug in list_location_slug:
            print('entrre en publicación - locacion')
            return reverse('properties:custom_list_publish_property', args=[publish_type, location_slug])
        elif (publish_type == 've' or publish_type == 'ar' or publish_type == 'at') and location_slug not in list_location_slug and property_type in list_property_type:
            print('entrre en publicación - propiedad')
            return reverse('properties:custom_list_publish_property', args=[publish_type, property_type])
        elif (publish_type == 've' or publish_type == 'ar' or publish_type == 'at') and location_slug not in list_location_slug and property_type not in list_property_type:
            return redirect('properties:custom_list_publish', args=[publish_type])
        elif (publish_type != 've' and publish_type != 'ar' and publish_type != 'at') and property_type not in list_property_type and location_slug in list_location_slug:
            return reverse('pages:home')
        elif (publish_type != 've' and publish_type != 'ar' and publish_type != 'at') and property_type in list_property_type and location_slug not in list_location_slug:
            return reverse('pages:home')
            
    except ObjectDoesNotExist:
        return reverse('properties:custom_list_publish_property', args=[publish_type, property_type])
    
    return False

def url_custom_list_publish_property(first_data, second_data):
    list_property_type = [i[0] for i in Property.PROPERTY_CHOICES]
    list_location_slug = [i.location_slug for i in Commune.objects.all()]
    properties = Property.objects.all()
    
    try:
        if (first_data != 've' and first_data != 'ar' and first_data != 'at') and first_data in list_property_type and second_data in list_location_slug:
            print('entrre en propiedad - locacion')
            qs = properties.filter(property_type=first_data, commune__location_slug=second_data)

            location_slug = [i.name for i in Commune.objects.all() if second_data in i.location_slug]
            entity = f'{[i for i in Property.PROPERTY_CHOICES][0][1]} en {location_slug[0]}'

            return qs, entity

        elif (first_data == 've' or first_data == 'ar' or first_data == 'at')  and second_data not in list_property_type and second_data in list_location_slug:
            print('entrre en publicación - locacion')
            qs = properties.filter(publish_type=first_data, commune__location_slug=second_data)

            location_slug = [i.name for i in Commune.objects.all() if second_data in i.location_slug]

            if first_data == 've':
                entity = f'Ventas en {location_slug[0]}'
            elif first_data == 'ar':
                entity = f'Arriendos en {location_slug[0]}'
            else:
                entity = f'Arriendos temporada en {location_slug[0]}'
            
            return qs, entity

        elif (first_data == 've' or first_data == 'ar' or first_data == 'at') and second_data in list_property_type and second_data not in list_location_slug:
            print('entrre en publicación - propiedad')
            qs = properties.filter(publish_type=first_data, property_type=second_data)

            if first_data == 've':
                entity = f'Ventas de {[i[1] for i in Property.PROPERTY_CHOICES if i[0] == second_data][0]}'
            elif first_data == 'ar':
                entity = f'Arriendos de {[i[1] for i in Property.PROPERTY_CHOICES if i[0] == second_data][0]}'
            else:
                entity = f'Arriendos temporada de {[i[1] for i in Property.PROPERTY_CHOICES if i[0] == second_data][0]}'

            return qs, entity

        elif (first_data == 've' or first_data == 'ar' or first_data == 'at') and second_data not in list_property_type and second_data not in list_location_slug:
            return reverse('properties:custom_list_publish', args=[first_data])

        else:
            # messages.error(request, 'Ha ocurrido un error inesperado')
            return reverse('pages:home')
    except Exception as e:
        print(str(e))
        return reverse('pages:home')

    