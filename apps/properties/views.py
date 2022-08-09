from itertools import chain
from operator import attrgetter
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView, View
from django.shortcuts import render, get_object_or_404, redirect
# from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages

from .models import House, HouseImage, Location, ApartmentImage, Apartment
from .forms import HouseForm, LocationForm, ApartmentForm
from apps.pages.forms import ContactForm

## -------------------------------------------------------------------------------------------------------------------------
#                                                        BASE VIEWS
## -------------------------------------------------------------------------------------------------------------------------
# class PropertyListView(View):
#     def get(self, request, *args, **kwargs):
#         properties =  Property.objects.filter(state=True)
#         q_publish = self.request.GET.get('q_publish')
#         q_property = self.request.GET.get('q_property')
#         if q_publish != None and q_property != None: 
#             properties = properties.filter(publish_type__icontains=q_publish, property_type__icontains=q_property)
#         paginator = Paginator(properties, 3)
#         page_number = self.request.GET.get('page')
#         properties_data = paginator.get_page(page_number)
#         context = {
#             'property_list': properties_data,
#             'page_obj': properties_data,
#             'q_publish': request.GET.get('q_publish', ''),
#             'q_property': request.GET.get('q_property', ''),
#         }
#         return render(request, 'properties/property_list.html', context)
    
class PropertyCustomListView(View):
    def get(self, request, *args, **kwargs):
        house = House.objects.all() 
        apartment = Apartment.objects.all() 
        properties_publish =  sorted(chain(house.filter(state=True), apartment.filter(state=True)), key=attrgetter('created_date'), reverse=True)
        properties_draft =  sorted(chain(house.filter(state=False), apartment.filter(state=False)), key=attrgetter('created_date'), reverse=True)
        # paginator = Paginator(properties, 9)
        # page_number = request.GET.get('page')
        # properties_data = paginator.get_page(page_number)
        context = {
            # 'property_list': properties_data,
            # 'page_obj': properties_data,
            'property_list_publish': properties_publish,
            'property_list_draft': properties_draft,
        }
        return render(request, 'properties/property_custom.html', context)

# class PropertyDetailView(View):
#     def get(self, request, *args, **kwargs):
#         property = get_object_or_404(Property, uuid=self.kwargs.get("uuid"))
#         context = {
#             'property': property,
#             'form' : ContactForm()
#         }
#         return render(request, 'properties/property_detail.html', context)

class LocationCreateView(View):
    def get(self, request, *args, **kwargs):
        form = LocationForm()
        context = {
            'form': form,
        }
        return render(request, 'properties/location_create.html', context)
    
    def post(self, request, *args, **kwargs):
        form = LocationForm(request.POST or None)
        if form.is_valid():
            instance = form.save()
            print(instance.uuid)
            uuid = instance.uuid
            return redirect(reverse('description_create', kwargs={'uuid': uuid}))
        messages.error(request, 'Fallo la creacion de la ubicación')
        return redirect('location_create')

class DescriptionCreateView(View):
    def get(self, request, uuid, *args, **kwargs):
        location = Location.objects.get(uuid=uuid)
        if location.property_type == 'ca':
            title = f'{location.street_address} {location.street_number}, {location.commune}'
            form = HouseForm(initial={'location': location, 'title': title})
        elif location.property_type == 'de':
            title = f'{location.street_address} {location.street_number}, {location.commune}'
            form = ApartmentForm(initial={'location': location, 'title': title})
        context = {
            'form': form
        }
        return render(request, 'properties/description_create.html', context)
    
    def post(self, request, uuid, *args, **kwargs):
        location = Location.objects.get(uuid=uuid)
        if location.property_type == 'ca':
            form = HouseForm(request.POST or None, request.FILES or None)
        elif location.property_type == 'de':
            form = ApartmentForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save()
            images = self.request.FILES.getlist('more_images')
            if location.property_type == 'ca':
                for i in images:
                    HouseImage.objects.create(house=instance, image=i)
            elif location.property_type == 'de':  
                for i in images:
                    ApartmentImage.objects.create(apartment=instance, image=i)
            return redirect('home')
        messages.error(request, form.errors)
        return redirect(reverse('description_create', kwargs={'uuid': uuid}))
               


# class PropertyUpdateView(View):
#     def get(self, request, *args, **kwargs):
#         property = get_object_or_404(Property, uuid=self.kwargs.get("uuid"))
#         form = PropertyForm(instance=property)
#         context = {
#             'form': form
#         }
#         return render(request, 'properties/property_edit.html', context)

#     def post(self, request, *args, **kwargs):
#         property = get_object_or_404(Property, uuid=self.kwargs.get("uuid"))
#         form = PropertyForm(request.POST, request.FILES or None, instance=property)
#         if form.is_valid():
#             instance = form.save()
#             images = self.request.FILES.getlist('more_images')
#             for i in images:
#                 PropertyImage.objects.create(property=instance, image=i)
#             return redirect('property_custom')
#         return render(request, 'properties/property_edit.html')

# class PropertyDeleteView(View):
#     def post(self, request, *args, **kwargs):
#         id = request.POST['id']
#         property = get_object_or_404(Property, id=id)
#         property.delete()
#         messages.success(request, "Propiedad eliminada correctamente")
#         return redirect('property_custom')

class HouseListView(View):
    def get(self, request, *args, **kwargs):
        q = self.request.GET.get('q', '')
        house = House.objects.filter(state=True)
        if q == '':
            paginator = Paginator(house, 1)
            page_number = self.request.GET.get('page')
            # print(page_number)
            qs = paginator.get_page(page_number)
        else:
            q_house = house.filter(publish_type__iexact=q)
            paginator = Paginator(q_house, 1)
            page_number = self.request.GET.get('page')
            # print(page_number)
            qs = paginator.get_page(page_number)
        context = {
            'page_obj': qs,
            'q': q,
            'entity': 'Casas'
        }
        return render(request, 'properties/house/house_list.html', context)

class HouseDetailView(View):
    def get(self, request, *args, **kwargs):
        house = get_object_or_404(House, uuid=self.kwargs.get("uuid"))
        context = {
            'property': house,
        }
        return render(request, 'properties/house/house_detail.html', context)

class ApartmentListView(View):
    def get(self, request, *args, **kwargs):
        q = self.request.GET.get('q', '')
        apartment = Apartment.objects.filter(state=True)
        if q == '':
            paginator = Paginator(apartment, 1)
            page_number = self.request.GET.get('page')
            # print(page_number)
            qs = paginator.get_page(page_number)
        else:
            q_apartment = apartment.filter(publish_type__iexact=q)
            paginator = Paginator(q_apartment, 1)
            page_number = self.request.GET.get('page')
            # print(page_number)
            qs = paginator.get_page(page_number)
        context = {
            'page_obj': qs,
            'q': q,
            'entity': 'Departamentos'
        }
        return render(request, 'properties/apartment/apartment_list.html', context)

class ApartmentDetailView(View):
    def get(self, request, *args, **kwargs):
        apartment = get_object_or_404(Apartment, uuid=self.kwargs.get("uuid"))
        context = {
            'property': apartment,
        }
        return render(request, 'properties/apartment/apartment_detail.html', context)


# class PropertyApartmentListView(View):
#     def get(self, request, *args, **kwargs):
#         q = self.request.GET.get('q', '')
#         apartment = Property.objects.filter(state=True, property_type='D')
#         print(q)
#         if q != '':
#             apartment = apartment.filter(publish_type__iexact=q)
#         context = {
#             'property_list': apartment
#         }
#         return render(request, 'properties/property_apartment_list.html', context)

