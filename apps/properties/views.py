from itertools import chain
from multiprocessing import context
from operator import attrgetter
from winreg import QueryValue
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView, View
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.core.exceptions import ViewDoesNotExist,BadRequest
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.text import slugify

from .filters import HouseFilter, ApartmentFilter

from .models import Commune, PropertyImage, Property, House,  Apartment
from .forms import PropertyForm, HouseForm, ApartmentForm
from apps.pages.forms import ContactForm






## -------------------------------------------------------------------------------------------------------------------------
#                                                        BASE VIEWS
## -------------------------------------------------------------------------------------------------------------------------

# class HouseListView(View):
#     def get(self, request, *args, **kwargs):
#         qs = House.objects.all()
#         q = qs

#         publish_type = request.GET.get('publish_type','')
#         sortBy = request.GET.get('sortBy','')
#         order = request.GET.get('order','')
#         min_bathroom = request.GET.get('min_bathroom','')
#         max_bathroom = request.GET.get('max_bathroom','')
#         min_room = request.GET.get('min_room','')
#         max_room = request.GET.get('max_room','')

        
#         # if publish_type:
#         #     q = qs.filter(property__publish_type=publish_type)

#         # elif sortBy == 'created':
#         #     q = house.order_by('created_date')
#         #     if order == 'desc':
#         #         q = house.order_by('-created_date')
                
#         # elif sortBy == 'title':
#         #     q = house.order_by('property__title')
#         #     if order == 'desc':
#         #         q = house.order_by('-property__title')

#         if min_room:
#             q = qs.filter(num_rooms__gte=min_room)

#         if max_room:
#             q = qs.filter(num_rooms__lt=max_room)

#         if min_bathroom:
#             q = qs.filter(num_bathrooms__gte=min_bathroom)

#         if max_bathroom:
#             q = qs.filter(num_bathrooms__lt=max_bathroom)



#         paginator = Paginator(q, 1)
#         page_number = self.request.GET.get('page')
#         page_obj = paginator.get_page(page_number)

    
       
#         context = {
#             'page_obj': page_obj,
#             'min_bathroom': min_bathroom,
#             'max_bathroom': max_bathroom,
#             'min_room': min_room,
#             'max_room': max_room,
#             'sortBy': sortBy,
#             'order': order,
#             'publish_type': publish_type,
#             'entity': 'Casas',
#         }
#         return render(request, 'properties/horizontal_list.html', context)

# class ApartmentListView(View):
#     def get(self, request, *args, **kwargs):
#         q = self.request.GET.get('q', '')
#         apartment = Apartment.objects.filter(state=True)
#         if q == '':
#             paginator = Paginator(apartment, 6)
#             page_number = self.request.GET.get('page')
#             # print(page_number)
#             qs = paginator.get_page(page_number)
#         else:
#             q_apartment = apartment.filter(publish_type__iexact=q)
#             paginator = Paginator(q_apartment, 1)
#             page_number = self.request.GET.get('page')
#             # print(page_number)
#             qs = paginator.get_page(page_number)
#         context = {
#             'page_obj': qs,
#             'q': q,
#             'entity': 'Departamentos'
#         }
#         return render(request, 'properties/horizontal_list.html', context)

# class PropertyCustomListView(View):
#     def get(self, request, *args, **kwargs):
#         house = House.objects.all() 
#         apartment = Apartment.objects.all() 
#         properties_publish =  sorted(chain(house.filter(state=True), apartment.filter(state=True)), key=attrgetter('created_date'), reverse=True)
#         properties_draft =  sorted(chain(house.filter(state=False), apartment.filter(state=False)), key=attrgetter('created_date'), reverse=True)
#         # paginator = Paginator(properties, 9)
#         # page_number = request.GET.get('page')
#         # properties_data = paginator.get_page(page_number)
#         context = {
#             # 'property_list': properties_data,
#             # 'page_obj': properties_data,
#             'property_list_publish': properties_publish,
#             'property_list_draft': properties_draft,
#         }
#         return render(request, 'properties/property_custom.html', context)
# class PropertyDetailView(View):
#     def get(self, request, *args, **kwargs):
#         property_type = self.kwargs.get("property_type")
#         slug = self.kwargs.get("slug")
#         if property_type == 'ca':
#             property = get_object_or_404(House, property__slug=slug)
#             property_image = property.property.properties.all()
#         elif property_type == 'de':
#             property = get_object_or_404(Apartment, property__slug=slug)
#             property_image = property.property.properties.all()
#         context = {
#             'property': property,
#             'property_image': property_image
#         }
#         return render(request, 'properties/property_detail.html', context)

def property_custom_list(request):
        properties = Property.objects.all()
        paginator = Paginator(properties, 1)
        page_number = request.GET.get('page')
        properties_data = paginator.get_page(page_number)
        context = {
            'page_obj': properties_data,
        }
        return render(request, 'properties/property_custom.html', context)

def property_detail(request, publish_type, property_type, location_slug, slug, uuid):
        property = Property.objects.get(uuid=uuid, location_slug=location_slug, slug=slug, publish_type=publish_type, property_type=property_type)
        if property_type == 'ca':
            property_especific = get_object_or_404(House, property=property)
            # property_image = property.properties.all()
        elif property_type == 'de':
            property_especific = get_object_or_404(Apartment, property=property)
            # property_image = property.properties.all()
        context = {
            'property': property_especific,
            'property_image': property.properties.all()
        }
        return render(request, 'properties/property_detail.html', context)

## -------------------------------------------------------------------------------------------------------------------------
#                                                        FUNCTION VIEWS
## -------------------------------------------------------------------------------------------------------------------------


def post(self, request, *args, **kwargs):
        try: 
            action  = request.POST['action']
            if action == 'delete':
                id = request.POST['id']
                property_type = request.POST['property_type']
                if property_type == 'ca':
                    # property = get_object_or_404(House, id=id)
                    # property.delete()
                    # property.save()
                    print('casita')
                elif property_type == 'de':
                    # property = get_object_or_404(House, id=id)
                    # property.delete()
                    # property.save()
                    print('depa')
                messages.success(request, "Propiedad eliminada correctamente")
            elif action == 'edit':
                pass
            elif action == 'publish':
                id = request.POST['id']
                property_type = request.POST['property_type']
                if property_type == 'ca':
                    property = get_object_or_404(House, id=id)
                    property.state = True
                    property.save()
                    print('casita')
                elif property_type == 'de':
                    property = get_object_or_404(Apartment, id=id)
                    property.state = True
                    property.save()
                    print('depa')
                messages.success(request, "Propiedad publicada correctamente")
            elif action == 'draft':
                id = request.POST['id']
                property_type = request.POST['property_type']
                if property_type == 'ca':
                    property = get_object_or_404(House, id=id)
                    property.state = False
                    property.save()
                    print('casita')
                elif property_type == 'de':
                    property = get_object_or_404(Apartment, id=id)
                    property.state = False
                    property.save()
                    print('depa')
                messages.success(request, "Propiedad despublicada correctamente")
            else:
                messages.error(request, "Ha ocurrido un error")
        except Exception as e:
            messages.alert(request, str(e))
        return redirect('property_custom')

def house_list(request):
    qs = House.objects.all()

    property__publish_type = request.GET.get('property__publish_type','')
    order = request.GET.get('order','')
    min_bathroom = request.GET.get('min_bathroom','')
    max_bathroom = request.GET.get('max_bathroom','')
    min_room = request.GET.get('min_room','')
    max_room = request.GET.get('max_room','')

    django_filter = HouseFilter(request.GET, queryset=qs)
    qs = django_filter.qs

    paginator = Paginator(qs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'min_bathroom': min_bathroom,
        'max_bathroom': max_bathroom,
        'min_room': min_room,
        'max_room': max_room,
        'order': order,
        'property__publish_type': property__publish_type,
        'entity': 'Casas',
        'django_filter': django_filter,
    }
    return render(request, 'properties/horizontal_list2.html', context)

def apartement_list(request):
    qs = Apartment.objects.all()

    property__publish_type = request.GET.get('property__publish_type','')
    order = request.GET.get('order','')
    min_bathroom = request.GET.get('min_bathroom','')
    max_bathroom = request.GET.get('max_bathroom','')
    min_room = request.GET.get('min_room','')
    max_room = request.GET.get('max_room','')

    django_filter = ApartmentFilter(request.GET, queryset=qs)
    qs = django_filter.qs

    paginator = Paginator(qs, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'min_bathroom': min_bathroom,
        'max_bathroom': max_bathroom,
        'min_room': min_room,
        'max_room': max_room,
        'order': order,
        'property__publish_type': property__publish_type,
        'entity': 'Casas',
        'django_filter': django_filter,
    }
    return render(request, 'properties/horizontal_list2.html', context)

def property_create(request, property_type):
    form = PropertyForm(request.POST or None, request.FILES or None, initial={'property_type': property_type})
    communes = Commune.objects.all()
    if property_type == 'ca':
        form_extra = HouseForm(request.POST or None)
    elif property_type == 'de':
        form_extra = ApartmentForm(request.POST or None)
    else:
        raise ViewDoesNotExist('Pagina no encontrada')
        # raise ValueError('Catagoria no encontrada')

    if request.method == 'POST':
        try:
            if form.is_valid and form_extra.is_valid:
                instance = form.save()
                property = Property.objects.get(id=instance.id)
                property.slug = slugify(property.title)
                property.location_slug = slugify(f"{property.commune}-{property.region}")
                property.save()
                form_extra.instance.property = property
                form_extra.save()
                images = request.FILES.getlist('more_images')
                for i in images:
                    PropertyImage.objects.create(property=instance, image=i)
                return redirect(reverse('property_detail', args=[property.publish_type, property.property_type, property.location_slug, property.slug, property.uuid]))
            else:
                messages.error(request, form.errors)
        except:
            # pass
            messages.error(request, form.errors)
    context = {
        'form': form,
        'form_extra': form_extra,
        'communes': communes,
    }
    return render(request, 'properties/property_create.html', context)

def property_update(request, property_type, region, slug, uuid):
    property = Property.objects.get(uuid=uuid)
    form = PropertyForm(request.POST or None, request.FILES or None, instance=property)
    communes = Commune.objects.filter(region__name=region)
    commune = property.commune
    if property.property_type == 'ca':
        house = House.objects.get(property=property)
        form_extra = HouseForm(request.POST or None, instance=house)
    elif property.property_type == 'de':
        apartment = Apartment.objects.get(property=property)
        form_extra = ApartmentForm(request.POST or None, instance=apartment)
    else:
        raise ViewDoesNotExist('Pagina no encontrada')
        # raise ValueError('Catagoria no encontrada')

    if request.method == 'POST':
        try:
            if form.is_valid and form_extra.is_valid:
                instance = form.save()
                property = Property.objects.get(id=instance.id)
                property.slug = slugify(property.title)
                property.save()
                form_extra.instance.property = property
                form_extra.save()
                images = request.FILES.getlist('more_images')
                for i in images:
                    PropertyImage.objects.create(property=instance, image=i)
                return redirect(reverse('property_detail', args=[property.property_type, property.region, property.slug, property.uuid]))
            # else:
            #     messages.error(request, 'ha ocurrido un error')
        except:
            # pass
            messages.error(request, form.errors)
    context = {
        'form': form,
        'form_extra': form_extra,
        'communes': communes,
        'commune_selected': commune,
    }
    return render(request, 'properties/property_create.html', context)

def property_delete(request, uuid, page_number):
    Property.objects.get(uuid=uuid).delete()
    # messages.success(request, "Propiedad eliminada correctamente")
    property_list = Property.objects.all()
    paginator = Paginator(property_list, 1)
    properties_data = paginator.get_page(page_number)
    return render(request, 'properties/partials/property_table.html', {'page_obj': properties_data})

def property_select(request):
    return render(request, 'properties/property_select.html')

def commune_select(request):
    region = request.GET.get('region', '')
    communes = Commune.objects.filter(region=region)
    return render(request, 'properties/partials/commune_select.html', {'communes': communes})

def custom_status(request, pk, action, page_number):
    property = get_object_or_404(Property, id=pk)
    print(pk, action)
    if action == 'draft':
        property.state = False
        property.save()

    if action == 'publish':
        property.state = True
        property.save()

    property_list = Property.objects.all()
    paginator = Paginator(property_list, 1)
    properties_data = paginator.get_page(page_number)
    return render(request, 'properties/partials/property_table.html', {'page_obj': properties_data})

def custom_table(request, page_number):
    q = request.POST.get('q', '')
    property_list = Property.objects.filter(commune_id__name__icontains=q)
    paginator = Paginator(property_list, 1)
    properties_data = paginator.get_page(page_number)
    return render(request, 'properties/partials/property_table.html', {'page_obj': properties_data}) 

## -------------------------------------------------------------------------------------------------------------------------
#                                                        FUNCTION VIEWS TESTING
## -------------------------------------------------------------------------------------------------------------------------

def custom_list(request, publish_type, property_type, location_slug):
    properties = Property.objects.filter(publish_type=publish_type, property_type=property_type, location_slug=location_slug)[0]
    print(properties.publish_type)
    entity = dict()
    entity['publish'] = properties.get_publish_type_display()
    entity['commune'] = properties.commune


    if property_type == 'ca':
        qs = House.objects.filter(property__publish_type=publish_type, property__property_type=property_type, property__location_slug=location_slug)
        entity['property'] = 'Casas'
    elif property_type == 'de':
        qs = Apartment.objects.filter(property__publish_type=publish_type, property__property_type=property_type, property__location_slug=location_slug)
        entity['property'] = 'Departamentos'
    property__publish_type = request.GET.get('property__publish_type','')
    order = request.GET.get('order','')
    min_bathroom = request.GET.get('min_bathroom','')
    max_bathroom = request.GET.get('max_bathroom','')
    min_room = request.GET.get('min_room','')
    max_room = request.GET.get('max_room','')

    django_filter = HouseFilter(request.GET, queryset=qs)
    qs = django_filter.qs

    paginator = Paginator(qs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(entity['publish'])

    context = {
        'page_obj': page_obj,
        'entity': entity,
        'min_bathroom': min_bathroom,
        'max_bathroom': max_bathroom,
        'min_room': min_room,
        'max_room': max_room,
        'order': order,
        'property__publish_type': property__publish_type,
        'django_filter': django_filter,
    }

    return render(request, 'properties/custom_list.html', context)