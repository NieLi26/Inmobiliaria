import re
from django import forms
from django.utils.text import slugify
from datetime import date

from multiselectfield import MultiSelectField

from .models import House, Property, Apartment, Commune, Region, PropertyContact
class PropertyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['type_price'].widget = forms.CheckboxSelectMultiple(choices=self.TYPE_PRICE_CHOICES)
        # for field in self.fields:
        #     self.fields[field].widget.attrs['autocomplete'] = "off"


    # more_images = forms.FileField(required=True, label='Mas Imagenes',widget=forms.ClearableFileInput(attrs={
    #     'multiple': True,
    #     'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'
    # }))



    class Meta:
        model = Property
        fields = (
            'property_type',
            'publish_type',
            'land_surface',
            'title',
            'description',
            'type_price',
            'price',
            'google_url',
            'video_url',
            'is_featured',
            'is_new',
            'thumbnail',
            'region',
            'commune',
            'street_address',
            'street_number',
            'slug',
            'realtor'
        )
        labels = {
            'realtor': 'Agente'
        }
        widgets ={
            # General
            'property_type': forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm', 'style': 'display:none'}),
            # 'publish_type': forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            # 'land_surface': forms.NumberInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md', "min": 0,'value':0}),
            # 'title': forms.TextInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'description': forms.Textarea(attrs={'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 mt-1 block w-full sm:text-sm border border-gray-300 rounded-md', 'rows': '3'}),
            # 'type_price': forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            # 'price': forms.NumberInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md', "min": 0,'value':0}),

            # Ubicación
            # 'region': forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm', 'hx-get': "'{% url 'commune_select' %}'", 'hx-trigger': 'change delay:500ms', 'hx-target': '#communes'}),
            # 'region': forms.Select(attrs={'class': 'border border-red-500 bg-white focus:outline-none border border-gray-300 rounded-lg py-2 px-4 block w-full appearance-none leading-normal text-gray-700', "hx-get": "/properties/commune_select", 'hx-trigger': 'change delay:500ms', 'hx-target': '#communes'}),
            'region': forms.Select(attrs={'class': 'bg-white focus:outline-none border border-gray-300 rounded-lg py-2 px-4 block w-full appearance-none leading-normal text-gray-700', "hx-get": "/properties/commune_select", 'hx-trigger': 'change delay:500ms', 'hx-target': '#communes'}),
            'commune': forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            # 'street_address': forms.TextInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            # 'street_number': forms.NumberInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            
            # url directions
            'google_url': forms.TextInput(attrs={'class': 'block w-full flex-1 rounded-none rounded-r-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm', 'placeholder': 'copiar enlace de incorporacion de mapa'}),
            # 'video_url': forms.TextInput(attrs={'class': 'block w-full flex-1 rounded-none rounded-r-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),

            # status
            # 'is_featured': forms.CheckboxInput(attrs={'class': 'focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded'}),
            # 'is_new': forms.CheckboxInput(attrs={'class': 'focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded'}),

            # Contact
            # 'phone1': forms.TextInput(attrs={'placeholder':'Ej. 945643233', 'data-mask': '(00) 000000000'}),
            # 'phone2': forms.TextInput(attrs={'placeholder':'Ej. 945643233'}),
            # 'email': forms.TextInput(attrs={'placeholder':'Ingrese su correo eléctronico'}),
        
            # imagen
            # 'thumbnail': forms.ClearableFileInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'})
        }

    # def clean_street_address(self):
    #     street_address = self.cleaned_data['street_address']
    #     if len(street_address) < 100:
    #         raise forms.ValidationError('Muy pocos parametros') 
    #     return street_address

    def clean_land_surface(self):
        land_surface = self.cleaned_data['land_surface']
        if land_surface <= 0:
            msg = 'Superficie de terreno debe ser mayor a cero'
            raise forms.ValidationError(msg) 
        return land_surface

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            msg = 'Precio debe ser mayor a cero'
            raise forms.ValidationError(msg) 
        return price

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        cleaned_data['slug'] = slugify(title)
        return cleaned_data

class HouseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for field in self.fields:
        #     if field == 'is_furnished':
        #         self.fields[field].widget.attrs["class"] = "focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
        #     else:
        #         self.fields[field].widget.attrs["class"] = "mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"

    # other = MultiSelectField(choices=OTHERS, max_length=50)
    
    # distribution = forms.MultipleChoiceField(label='Distribución', widget=forms.CheckboxSelectMultiple(choices=Property.Distributions.choices))
    class Meta:
        model = House
        exclude = ("state",)

    def clean_builded_year(self):
        builded_year = self.cleaned_data['builded_year']
        if builded_year > date.today().year:
            msg = 'El año de construcción debe ser igual o inferior al actual'
            raise forms.ValidationError(msg)
        return builded_year

    def clean_num_rooms(self):
        num_rooms = self.cleaned_data['num_rooms']
        if num_rooms > 15:
            msg = 'La cantidad debe ser igual o inferior a 15'
            raise forms.ValidationError(msg)
        return num_rooms


    def clean_builded_surface(self):
        builded_surface = self.cleaned_data['builded_surface']
        if builded_surface <= 0:
            msg = 'Superficie construida debe ser mayor a cero'
            raise forms.ValidationError(msg) 
        return builded_surface

class ApartmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for field in self.fields:
        #     if field == 'is_furnished':
        #         self.fields[field].widget.attrs["class"] = "focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
        #     else:
        #         self.fields[field].widget.attrs["class"] = "mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
    class Meta:
        model = Apartment
        exclude = ("state", "property")


    def clean_builded_year(self):
        builded_year = self.cleaned_data['builded_year']
        if builded_year > date.today().year:
            msg = 'El año de construcción debe ser igual o inferior al actual'
            raise forms.ValidationError(msg)
        return builded_year

    def clean_num_rooms(self):
        num_rooms = self.cleaned_data['num_rooms']
        if num_rooms > 15:
            msg = 'La cantidad debe ser igual o inferior a 15'
            raise forms.ValidationError(msg)
        return num_rooms


    def clean_builded_surface(self):
        builded_surface = self.cleaned_data['builded_surface']
        if builded_surface <= 0:
            msg = 'Superficie construida debe ser mayor a cero'
            raise forms.ValidationError(msg) 
        return builded_surface

class PropertyContactForm(forms.ModelForm):
    

    class Meta:
        model = PropertyContact
        fields = ('name', 'from_email', 'phone', 'message')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        patron = '^[0-9]+$'
        print(re.search(patron, phone))
        if re.search(patron, phone) == None and phone != '' :
            raise forms.ValidationError('Solo debe ingresar numeros')
        return phone