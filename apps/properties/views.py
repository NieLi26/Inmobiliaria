import os
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy,reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.core.exceptions import ViewDoesNotExist
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils.text import slugify
from django.db import transaction
from django.views.generic import ListView, View, CreateView, UpdateView, DeleteView, DetailView
from django.template.loader import get_template

from render_block import render_block_to_string

#test decorator
from .decorators import url_custom_list_decorator
from .utils import url_custom_list_publish_property

# remove file storage
from django.core.files.storage import FileSystemStorage

#cache
from django.views.decorators.cache import cache_control

from .filters import PropertyFilter

from .models import Commune, PropertyImage, Property, House,  Apartment, PropertyContact, Realtor
from .forms import PropertyForm, HouseForm, ApartmentForm, PropertyContactForm



# CRUD ARRENDATARIO 
class RealtorCreateView(CreateView):
    model = Realtor
    fields = ['first_name', 'last_name', 'phone1', 'phone2', 'email']
    template_name = 'properties/realtor_create.html'
    success_url = reverse_lazy('properties:realtor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación'
        return context

class RealtorUpdateView(UpdateView):
    model = Realtor
    fields = ['first_name', 'last_name', 'phone1', 'phone2', 'email']
    template_name = 'properties/realtor_create.html'
    success_url = reverse_lazy('properties:realtor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modificación'
        return context

class RealtorListView(ListView):
    model = Realtor
    template_name = 'properties/realtor_list.html'
    paginate_by = 1
    context_object_name = 'object_list'
    page_kwarg = 'page_obj'

    def get_queryset(self):
        return  Realtor.objects.filter(state=True)

class RealtorDetailView(DetailView):
    model = Realtor
    template_name = 'properties/realtor_detail.html'

# partials
class TableRealtorView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        print('hola')
        realtors = Realtor.objects.filter(state=True)
        realtors = realtors.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q))
        paginator = Paginator(realtors, 1)
        realtors_data = paginator.get_page(kwargs['page_number'])
        print(realtors_data.object_list)
        context = {
            'object_list': realtors_data.object_list, 
            'page_obj': realtors_data, 
            'q': q
        }
        html = render_block_to_string('properties/realtor_list.html', 'table_list', context)
        return HttpResponse(html)

class RealtorDeleteView(View):
    def get(self, request, *args, **kwargs):
        realtor = Realtor.objects.get(id=kwargs['pk'])
        realtor.state = False
        realtor.save()
        print('feo')
        realtors = Realtor.objects.filter(state=True)
        paginator = Paginator(realtors, 1)
        realtors_data = paginator.get_page(kwargs['page_number'])

        context = {
            'object_list': realtors_data.object_list, 
            'page_obj': realtors_data, 
        }
        html = render_block_to_string('properties/realtor_list.html', 'table_list', context)
        return HttpResponse(html)


## CRUD CONTACT
class PropertyContactListView(ListView):
    model = PropertyContact
    template_name = 'properties/contact_list.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_title'] = 'Contactos'
        context['sidebar_subtitle'] = 'Maneja la información de contactos de propiedades!'
        return context

# testing change page_number in CBV(List View)
# class TableContactListView(ListView):
#     model = PropertyContact
#     template_name = 'properties/partials/contact_table.html'
#     paginate_by = 2

#     def get_queryset(self):
#         q = self.request.GET.get('q', '')
#         print(q)
#         contact_list = PropertyContact.objects.filter(name__icontains=q)
#         return contact_list

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['paginator_class'] = self.get_paginator(self.queryset, 2)
#         return context
class TableContactView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
    
        contact_list = PropertyContact.objects.filter(name__icontains=q)
        print(contact_list)
        paginator = Paginator(contact_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            # 'contact_list': properties_data,
            'page_obj': properties_data,
            'q': q
        }
        html = render_block_to_string('properties/contact_list.html', 'table_list', context)
        return HttpResponse(html)

class ModalContactView(View):
    def get(self, request, *args, **kwargs):
        contact = PropertyContact.objects.get(id=kwargs['pk'])
        contact.state = False
        contact.save()
        contact_list = PropertyContact.objects.all()
        paginator = Paginator(contact_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': properties_data,
        }
        html = render_block_to_string('properties/contact_list.html', 'table_list', context)
        return HttpResponse(html)



def contact_detail_form(request, publish_type, property_type, location_slug, slug, uuid):
    property = Property.objects.get(uuid=uuid, commune__location_slug=location_slug, slug=slug, publish_type=publish_type, property_type=property_type)
    if property_type == 'ca':
        property_especific = get_object_or_404(House, property=property)
        message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.houses.first().num_rooms} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

    elif property_type == 'de':
        property_especific = get_object_or_404(Apartment, property=property)
        message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.apartments.first().num_rooms} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

    form = PropertyContactForm(request.POST or None, initial={'message': message}) # no se puede asignar valor  de inicio a un elemento excluido
    if form.is_valid():
        form.instance.property = property
        form.save() 
        
        context = {
            'form': PropertyContactForm(initial={'message': message}),
            'property': property_especific
        }
        html = render_block_to_string('properties/property_detail.html', 'contact_detail', context)
        response =  HttpResponse(html)
        response['HX-Trigger'] = 'modal-contact-button'
        return response

    context = {
        'property': property_especific,
        'form': form,
    }
    html = render_block_to_string('properties/property_detail.html', 'contact_detail', context)
    return HttpResponse(html)



## CRUD PROPIEDAD DESPUBLICADA

class DraftListView(ListView):
    template_name = 'properties/property_custom.html'
    queryset = Property.objects.filter(state=False)
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['url_option'] = 'table_draft'
        context['sidebar_title'] = 'Propiedades'
        context['sidebar_subtitle'] = 'Maneja la información de tus propiedades despublicadas!'
        return context

class DraftFeaturedView(View):
    def get(self, request, *args, **kwargs):
        property = get_object_or_404(Property, id=kwargs['pk'])

        if kwargs['action'] == 'normal':
            property.is_featured = False
            property.save()

        if kwargs['action']  == 'featured':
            property.is_featured = True
            property.save()

        property_list = Property.objects.filter(state=False)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': properties_data, 
            'url_option': 'table_draft'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


class DraftStatusView(View):
    def get(self, request, *args, **kwargs):
        property = get_object_or_404(Property, id=kwargs['pk'])
      
        if kwargs['action'] == 'draft':
            property.state = False
            property.save()

        if kwargs['action']  == 'publish':
            property.state = True
            property.save()

        property_list = Property.objects.filter(state=False)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        context = {
            'page_obj': properties_data, 
            'url_option': 'table_draft'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


class DraftDeleteView(View):
    def get(self, request, *args, **kwargs):
        Property.objects.get(uuid=kwargs['uuid']).delete()
        # messages.success(request, "Propiedad eliminada correctamente")
        property_list = Property.objects.filter(state=False)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])

        context = {
            'page_obj': properties_data, 
            'url_option': 'table_draft'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)


# paginator
class TableDraftView(View): # probe como pasar template y context con httpresponse en vez de render
    def get(sefl, request, *args, **kwargs):
        q = request.GET.get('q', '')
        
        property_list = Property.objects.filter(commune_id__name__icontains=q, state=False)
        paginator = Paginator(property_list, 2)
        properties_data = paginator.get_page(kwargs['page_number'])
        # template = get_template('properties/partials/property_table.html')
        context = {
            'page_obj': properties_data, 
            'q': q,
            'url_option': 'table_draft'
        }
        html = render_block_to_string('properties/property_custom.html', 'table_list', context)
        return HttpResponse(html)
        # return HttpResponse(template.render(context), content_type='html')



## CRUD PROPIEDADES PUBLICADAS

def property_publish_list(request):
        properties = Property.objects.filter(state=True)
        paginator = Paginator(properties, 2)
        page_number = request.GET.get('page')
        properties_data = paginator.get_page(page_number)
        context = {
            'page_obj': properties_data,
            'url_option': 'table_publish',
            'sidebar_title' : 'Propiedades',
            'sidebar_subtitle' : 'Maneja la información de tus propiedades publicadas!',
        }
        return render(request, 'properties/property_custom.html', context)

# partials
def publish_featured(request, pk, action, page_number):
    property = get_object_or_404(Property, id=pk)

    if action == 'normal':
        property.is_featured = False
        property.save()

    if action == 'featured':
        property.is_featured = True
        property.save()

    property_list = Property.objects.filter(state=True)
    paginator = Paginator(property_list, 2)
    properties_data = paginator.get_page(page_number)
    context = {
        'page_obj': properties_data, 
        'url_option': 'table_publish'
    }
    html = render_block_to_string('properties/property_custom.html', 'table_list', context)
    return HttpResponse(html)


def publish_status(request, pk, action, page_number):
    property = get_object_or_404(Property, id=pk)
   
    if action == 'draft':
        property.state = False
        property.save()

    if action == 'publish':
        property.state = True
        property.save()

    property_list = Property.objects.filter(state=True)
    paginator = Paginator(property_list, 2)
    properties_data = paginator.get_page(page_number)

    context = {
        'page_obj': properties_data, 
        'url_option': 'table_publish'
    }
    html = render_block_to_string('properties/property_custom.html', 'table_list', context)
    return HttpResponse(html)
 

def publish_delete(request, uuid, page_number):
    Property.objects.get(uuid=uuid).delete()
    # messages.success(request, "Propiedad eliminada correctamente")
    property_list = Property.objects.filter(state=True)
    paginator = Paginator(property_list, 2)
    properties_data = paginator.get_page(page_number)

    context = {
        'page_obj': properties_data, 
        'url_option': 'table_publish'
    }
    html = render_block_to_string('properties/property_custom.html', 'table_list', context)
    return HttpResponse(html)


def table_publish(request, page_number):
    q = request.GET.get('q', '')

    property_list = Property.objects.filter(commune_id__name__icontains=q, state=True)
    paginator = Paginator(property_list, 2)
    properties_data = paginator.get_page(page_number)
    context = {
        'page_obj': properties_data, 
        'q': q,
        'url_option': 'table_publish',
    }
    html = render_block_to_string('properties/property_custom.html', 'table_list', context)
    return HttpResponse(html)


## GENERAL PUBLICACIONES

class PropertyGaleryView(View):

    """ Galeria para agregar y eliminar imagenes de detalle de propiedad """
    
    def get(self, request, *args, **kwargs):
        property = Property.objects.get(slug=kwargs['slug'], uuid=kwargs['uuid'])
        property_images = PropertyImage.objects.filter(property=property)
        context = {
            'property_images': property_images,
            'property': property
        }
        return render(request, 'properties/property_galery.html', context)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # action = json.loads(request.body)['action']
            action = request.POST['action']
            if action == 'delete':
                id = request.POST['id']
                property_image = PropertyImage.objects.get(id=id)
                ## metodo para eliminar archivos 

                # image = str(property_image.image
                # image = property_image.image.url
                image = property_image.image.path
                
                # 1) Sirve con todas
                fs = FileSystemStorage()
                fs.delete(image)
                property_image.delete()

                # 2) Solo sirve con "path"
                # if os.path.isfile(image):
                #     os.remove(image)
                #     property_image.delete()

                # retornar previsualización personalizada
                property = Property.objects.get(slug=kwargs['slug'], uuid=kwargs['uuid'])
                preview_images = PropertyImage.objects.filter(property=property)
                preview_images = [i.toJSON() for i in preview_images]

                data = {
                    'preview_images': preview_images
                }
            if action == 'create':
                id = request.POST.get('id')
                imagen = request.FILES.get('imagen')
                property_image = PropertyImage.objects.create(property_id=id, image=imagen)

                # retornar previsualización personalizada
                property = Property.objects.get(slug=kwargs['slug'], uuid=kwargs['uuid'])
                preview_images = PropertyImage.objects.filter(property=property)
                preview_images = [i.toJSON() for i in preview_images]
             
                data = {
                    'id': property_image.id,
                    'property_image': str(property_image.image),
                    'preview_images': preview_images
                }
                # return redirect('properties:property_detail', args=[property.publish_type, property.property_type, property.commune.location_slug, property.slug, property.uuid])
            else:
                data['error']  = 'Ha ocurrido un error'
        except Exception as e:
            # print(str(e))
            data['error'] = str(e)
        return JsonResponse(data)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def property_detail(request, publish_type, property_type, location_slug, slug, uuid):
        property = Property.objects.get(uuid=uuid, commune__location_slug=location_slug, slug=slug, publish_type=publish_type, property_type=property_type)
        if property_type == 'ca':
            property_especific = get_object_or_404(House, property=property)
            message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.houses.first().num_rooms} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

        elif property_type == 'de':
            property_especific = get_object_or_404(Apartment, property=property)
            message = f'Hola , Estoy interesado en {property.get_property_type_display()} en {property.get_publish_type_display()} de {property.apartments.first().num_rooms} Dormitorios En {property.commune.name}, por favor comunícate conmigo. ¡Gracias!'

        form = PropertyContactForm(request.POST or None, initial={'message': message}) # no se puede asignar valor  de inicio a un elemento excluido
        context = {
            'property': property_especific,
            'property_image': property.properties.all(),
            'form': form,
            'wa_message': property.title,
            'wa_number': '56968462368'
        }
        return render(request, 'properties/property_detail.html', context)


def property_create(request, property_type):
    form = PropertyForm(request.POST or None, request.FILES or None, initial={'property_type': property_type})
    communes = Commune.objects.all()
    commune = ''
    disabled = True

    if request.POST.get('region'):
        communes = communes.filter(region=request.POST.get('region'))
        disabled = False


    if request.POST.get('commune'):
        commune = communes.get(id=request.POST.get('commune'))
        disabled = False

    if property_type == 'ca':
        form_extra = HouseForm(request.POST or None)
    elif property_type == 'de':
        form_extra = ApartmentForm(request.POST or None)
    else:
        raise ViewDoesNotExist('Pagina no encontrada')
        # raise ValueError('Catagoria no encontrada')


    if request.method == 'POST':
        # try:
        if form.is_valid() and form_extra.is_valid():
            with transaction.atomic(): # para realizar uno o mas queries seguros, sino se hace un rollback, pero con 2 o mas ses habitual usarlos, si uno falla, se anula todo
                instance = form.save()
                extra_instance = form_extra.save(commit=False)
                extra_instance.property = instance
                extra_instance.save()
                # images = request.FILES.getlist('more_images')
                # for i in images:
                #     PropertyImage.objects.create(property=instance, image=i)
                return redirect(reverse('properties:property_galery', args=[instance.slug, instance.uuid]))
        # else:
        #     messages.error(request, form_extra.errors)
        #     messages.error(request, form.errors)
        # except:
        #     pass
            # messages.error(request, form_extra.errors)
            # messages.error(request, form.errors)
    context = {
        'form': form,
        'form_extra': form_extra,
        'communes': communes,
        'commune_selected': commune,
        'disabled': disabled,
    }
    return render(request, 'properties/property_create.html', context)



def property_update(request, slug, uuid):
    property = Property.objects.get(uuid=uuid, slug=slug)
    form = PropertyForm(request.POST or None, request.FILES or None, instance=property)

    communes = Commune.objects.all()

    if request.POST.get('region'):
        communes = communes.filter(region=request.POST.get('region'))
    else:
        communes = communes.filter(region=property.region)

    if request.POST.get('commune'):
        commune = communes.get(id=request.POST.get('commune'))
    else:
        commune = property.commune

    if property.property_type == 'ca':
        house = House.objects.get(property=property)
        form_extra = HouseForm(request.POST or None, instance=house)
    elif property.property_type == 'de':
        apartment = Apartment.objects.get(property=property.id)
        form_extra = ApartmentForm(request.POST or None, instance=apartment)
    # else:
    #     raise ViewDoesNotExist('Pagina no encontrada')
    #     # raise ValueError('Catagoria no encontrada')

    if request.method == 'POST':
        # try:
        if form.is_valid and form_extra.is_valid:
            with transaction.atomic(): # para realizar uno o mas queries seguros, sino se hace un rollback, pero con 2 o mas ses habitual usarlos, si uno falla, se anula todo
                instance = form.save()
                extra_instance = form_extra.save(commit=False)
                extra_instance.property = instance
                extra_instance.save()
                return redirect('properties:property_galery', property.slug, property.uuid)
            # else:
            #     messages.error(request, 'ha ocurrido un error')
        # except:
        #     # pass
        #     messages.error(request, form.errors)
    context = {
        'form': form,
        'form_extra': form_extra,
        'communes': communes,
        'commune_selected': commune,
        # 'disabled': False,
    }
    return render(request, 'properties/property_create.html', context)


def property_select(request):
    return render(request, 'properties/property_select.html')


def commune_select(request):

    region = request.GET.get('region', '')

    communes = Commune.objects.all()
    if region != '':
        communes = communes.filter(region=region)
        disabled = False
    else:
        disabled = True
    context = {
        'communes': communes,
        'disabled': disabled,
    }
    html = render_block_to_string('properties/property_create.html', 'commune', context)
    return HttpResponse(html)
    # return render(request, 'properties/property_create.html', context)



## -------------------------------------------------------------------------------------------------------------------------
#                                                        FBV TESTING ADAPTING PROPERTY LIST
## -------------------------------------------------------------------------------------------------------------------------



#1
@url_custom_list_decorator
def custom_list(request, publish_type, property_type, location_slug):

    if publish_type == 've':
        entity = f'Ventas de {[i[1] for i in Property.PROPERTY_CHOICES if i[0] == property_type][0]} en {[i.name for i in Commune.objects.all() if location_slug == i.location_slug][0]}' 
    elif publish_type == 'ar':
        entity = f'Arriendos de {[i[1] for i in Property.PROPERTY_CHOICES if i[0] == property_type][0]} en {[i.name for i in Commune.objects.all() if location_slug == i.location_slug][0]}' 
    elif publish_type == 'at':
        entity = f'Arriendos temporada de {[i[1] for i in Property.PROPERTY_CHOICES if i[0] == property_type][0]} en {[i.name for i in Commune.objects.all() if location_slug == i.location_slug][0]}' 
    elif publish_type == 'pe':
        entity = f'Permutas de {[i[1] for i in Property.PROPERTY_CHOICES if i[0] == property_type][0]} en {[i.name for i in Commune.objects.all() if location_slug == i.location_slug][0]}' 

    qs = Property.objects.filter(publish_type=publish_type, property_type=property_type, commune__location_slug=location_slug)


    django_filter = PropertyFilter(request.GET, queryset=qs)
    qs = django_filter.qs

    paginator = Paginator(qs, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'entity': entity,
        'django_filter': django_filter,
        'publish_type': publish_type,
        'property_type': property_type,
        'location_slug': location_slug,
    }

    return render(request, 'properties/property_list.html', context)

@url_custom_list_decorator
def property_list(request, page_number, publish_type, property_type, location_slug):

    if publish_type == 've':
        entity = f'Ventas de {[i[1] for i in Property.PROPERTY_CHOICES if i[0] == property_type][0]} en {[i.name for i in Commune.objects.all() if location_slug == i.location_slug][0]}' 
    elif publish_type == 'ar':
        entity = f'Arriendos de {[i[1] for i in Property.PROPERTY_CHOICES if i[0] == property_type][0]} en {[i.name for i in Commune.objects.all() if location_slug == i.location_slug][0]}' 
    elif publish_type == 'at':
        entity = f'Arriendos temporada de {[i[1] for i in Property.PROPERTY_CHOICES if i[0] == property_type][0]} en {[i.name for i in Commune.objects.all() if location_slug == i.location_slug][0]}' 
    elif publish_type == 'pe':
        entity = f'Permutas de {[i[1] for i in Property.PROPERTY_CHOICES if i[0] == property_type][0]} en {[i.name for i in Commune.objects.all() if location_slug == i.location_slug][0]}' 

    qs = Property.objects.filter(publish_type=publish_type, property_type=property_type, commune__location_slug=location_slug)

    print(request.GET.get('price_option',''))
    property__publish_type = request.GET.get('property__publish_type','')
    order = request.GET.get('order','')
    min_bathroom = request.GET.get('min_bathroom','')
    max_bathroom = request.GET.get('max_bathroom','')
    min_room = request.GET.get('min_room','')
    max_room = request.GET.get('max_room','')
    price__gte = request.GET.get('price__gte','')
    price__lte = request.GET.get('price__lte','')
    type_price = request.GET.get('type_price','')

    django_filter = PropertyFilter(request.GET, queryset=qs)
    qs = django_filter.qs

    paginator = Paginator(qs, 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'entity': entity,

        'min_bathroom': min_bathroom,
        'max_bathroom': max_bathroom,
        'min_room': min_room,
        'max_room': max_room,
        'price__gte': price__gte,
        'price__lte': price__lte,
        'type_price': type_price,
        'order': order,
        'property__publish_type': property__publish_type,

        'django_filter': django_filter,
        'publish_type': publish_type,
        'property_type': property_type,
        'location_slug': location_slug,
    }
    html = render_block_to_string('properties/property_list.html', 'post', context)
    return HttpResponse(html)

#2
def custom_list_publish_property(request, first_data, second_data):
    print('Dentre')
    response = url_custom_list_publish_property(first_data, second_data)

    if len(response) == 2:
        qs = response[0]
        entity = response[1]
    else:
        return redirect(response)

    django_filter = PropertyFilter(request.GET, queryset=qs)
    qs = django_filter.qs

    paginator = Paginator(qs, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'page_obj': page_obj,
        'entity': entity,
        'django_filter': django_filter,
        'first_data': first_data,
        'second_data': second_data,
    }

    return render(request, 'properties/property_list_publish_property.html', context)

def property_list_publish_property(request, page_number, first_data, second_data):

    response = url_custom_list_publish_property(first_data, second_data)

    if len(response) == 2:
        qs = response[0]
        entity = response[1]
    else:
        return redirect(response)

    property__publish_type = request.GET.get('property__publish_type','')
    order = request.GET.get('order','')
    min_bathroom = request.GET.get('min_bathroom','')
    max_bathroom = request.GET.get('max_bathroom','')
    min_room = request.GET.get('min_room','')
    max_room = request.GET.get('max_room','')
    price__gte = request.GET.get('price__gte','')
    price__lte = request.GET.get('price__lte','')
    type_price = request.GET.get('type_price','')

    django_filter = PropertyFilter(request.GET, queryset=qs)
    qs = django_filter.qs

    paginator = Paginator(qs, 1)
    page_obj = paginator.get_page(page_number)


    context = {
        'page_obj': page_obj,
        'entity': entity,

        'min_bathroom': min_bathroom,
        'max_bathroom': max_bathroom,
        'min_room': min_room,
        'max_room': max_room,
        'price__gte': price__gte,
        'price__lte': price__lte,
        'type_price': type_price,
        'order': order,
        'property__publish_type': property__publish_type,

        'django_filter': django_filter,
        'first_data': first_data,
        'second_data': second_data,
    }
    html = render_block_to_string('properties/property_list_publish_property.html', 'post_publish_property', context)
    return HttpResponse(html)


#3
def custom_list_publish(request, publish_type):
    print(publish_type)
    try:
        if publish_type == 've' or publish_type == 'ar' or publish_type == 'at' or publish_type == 'pe':
            qs = Property.objects.filter(publish_type=publish_type, state=True)
        else:
            return redirect('pages:home')
    except Exception as e:
        print(str(e))
        return redirect('pages:home')


    if publish_type == 've':
        entity = 'Inmuebles en Venta'
    if publish_type == 'ar':
        entity = 'Inmuebles en Arriendo'
    if publish_type == 'at':
        entity = 'Inmuebles en Arriendo temporada'
    if publish_type == 'pe':
        entity = 'Inmuebles en Permuta'

    django_filter = PropertyFilter(request.GET, queryset=qs)
    qs = django_filter.qs

    paginator = Paginator(qs, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'entity': entity,
        'django_filter': django_filter,
        'publish_type': publish_type
    }

    return render(request, 'properties/property_list_publish.html', context)

def property_list_publish(request, page_number, publish_type):
    try:
        if publish_type == 've' or publish_type == 'ar' or publish_type == 'at' or publish_type == 'pe':
            qs = Property.objects.filter(publish_type=publish_type, state=True)
        else:
            return redirect('pages:home')
    except Exception as e:
        print(str(e))
        return redirect('pages:home')


    if publish_type == 've':
        entity = 'Inmuebles en Venta'
    if publish_type == 'ar':
        entity = 'Inmuebles en Arriendo'
    if publish_type == 'at':
        entity = 'Inmuebles en Arriendo temporada'
    if publish_type == 'pe':
        entity = 'Inmuebles en Permuta'

    property__publish_type = request.GET.get('property__publish_type','')
    order = request.GET.get('order','')
    min_bathroom = request.GET.get('min_bathroom','')
    max_bathroom = request.GET.get('max_bathroom','')
    min_room = request.GET.get('min_room','')
    max_room = request.GET.get('max_room','')
    price__gte = request.GET.get('price__gte','')
    price__lte = request.GET.get('price__lte','')
    type_price = request.GET.get('type_price','')

    
    django_filter = PropertyFilter(request.GET, queryset=qs)
    qs = django_filter.qs
    paginator = Paginator(qs, 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'entity': entity,

        'price__gte': price__gte,
        'price__lte': price__lte,
        'min_bathroom': min_bathroom,
        'max_bathroom': max_bathroom,
        'min_room': min_room,
        'max_room': max_room,
        'type_price': type_price,
        'order': order,
        'property__publish_type': property__publish_type,

        'django_filter': django_filter,
        'publish_type': publish_type
    }
    html = render_block_to_string('properties/property_list_publish.html', 'post_publish', context)
    return HttpResponse(html)




        # try: 
        #     action  = request.POST['action']
        #     if action == 'delete':
        #         id = request.POST['id']
        #         property_type = request.POST['property_type']
        #         if property_type == 'ca':
        #             # property = get_object_or_404(House, id=id)
        #             # property.delete()
        #             # property.save()
        #             print('casita')
        #         elif property_type == 'de':
        #             # property = get_object_or_404(House, id=id)
        #             # property.delete()
        #             # property.save()
        #             print('depa')
        #         messages.success(request, "Propiedad eliminada correctamente")
        #     elif action == 'edit':
        #         pass
        #     elif action == 'publish':
        #         id = request.POST['id']
        #         property_type = request.POST['property_type']
        #         if property_type == 'ca':
        #             property = get_object_or_404(House, id=id)
        #             property.state = True
        #             property.save()
        #             print('casita')
        #         elif property_type == 'de':
        #             property = get_object_or_404(Apartment, id=id)
        #             property.state = True
        #             property.save()
        #             print('depa')
        #         messages.success(request, "Propiedad publicada correctamente")
        #     elif action == 'draft':
        #         id = request.POST['id']
        #         property_type = request.POST['property_type']
        #         if property_type == 'ca':
        #             property = get_object_or_404(House, id=id)
        #             property.state = False
        #             property.save()
        #             print('casita')
        #         elif property_type == 'de':
        #             property = get_object_or_404(Apartment, id=id)
        #             property.state = False
        #             property.save()
        #             print('depa')
        #         messages.success(request, "Propiedad despublicada correctamente")
        #     else:
        #         messages.error(request, "Ha ocurrido un error")
        # except Exception as e:
        #     messages.alert(request, str(e))
        # return redirect('property_custom')