import re
import random
from django import forms
from django.utils.text import slugify
from datetime import date
from django.core.validators import RegexValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import House, Property, Apartment, Commune, Region, PropertyContact, Realtor, Owner

# Every letter to LowerCase(charfield)
class LowerCase(forms.CharField):
    def to_python(self, value):
        return value.lower()

# Every letter to UpperCase(charfield)
class UpperCase(forms.CharField):
    def to_python(self, value):
        return value.upper()

number_validator = RegexValidator(
    regex=r'^[1-9]\d*$',
    message= [
        'Este campo solo debe contener números.',
        'Debe ser mayor a 0.'
    ]
)

attrs_class = 'focus:outline-none border border-gray-300 rounded-lg py-2 px-4 block w-full appearance-none leading-normal text-gray-700'
attrs_class_error = 'focus:outline-none border border-red-500 rounded-lg py-2 px-4 block w-full appearance-none leading-normal text-gray-700'

class PropertyForm(forms.ModelForm):
    # se le puede poner cualquier nombre, y cualquier texto, y se llama con el nombre del contexto como pasaste el form.nombre de la variable(ej. form.required_css_class)
    required_css_class = 'focus:outline-none border border-gray-300 rounded-lg py-2 px-4 block w-full appearance-none leading-normal text-gray-700' 

    # si no creara este atributo solo me denegaria automaticamente el valor que no es numero, y me diria siempre "el valor es requerido"
    price = forms.CharField(label='Precio Publicación', validators=[number_validator], help_text='Este es un texto de ayuda! ir a <a href="/">Home<a/>')
    appraisal_value = forms.CharField(label='Valor Tasación', validators=[number_validator])
    commission_percentage = forms.CharField(label='Porcentaje Comision', validators=[number_validator])
    commission_value = forms.CharField(label='Valor Comision', validators=[number_validator])
    google_url = forms.CharField(label='Google url', widget=forms.TextInput(attrs={'placeholder': 'copiar enlace de incorporacion de mapa'}), required=False)
    # price = forms.RegexField(regex=r'^[0-9]*$', error_messages={'invalid': 'Este campo solo debe contener números.', 'invalid_choice': 'Este campo solo debe contener números.'})

    def __init__(self, *args, **kwargs):
        property_type=kwargs.pop('property_type', None) 
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'is_featured' and field != 'is_new' and field != 'is_iva':
                self.fields[field].widget.attrs['class'] = attrs_class
            else:
                self.fields[field].widget.attrs["class"] = "focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
            # if self.errors.get(field) and self.fields[field].widget.attrs.get('class'):
            if self.errors.get(field):
                self.fields[field].widget.attrs['class'] = attrs_class_error

        self.fields['description'].widget.attrs['rows'] = '3'
        # self.fields['property_type'].widget.attrs['style'] = 'display:none'
        self.fields['property_type'].widget.attrs.update(style='display:none')
        self.fields['property_type'].initial = property_type

        self.fields['price'].widget.attrs['x-mask:dynamic'] = '$money($input)' # no funciona en todos
        # self.fields['price'].validators = [RegexValidator(r'^[0-9]*$', message='Solo numeros son permitidos')]

        selects = ['owner', 'realtor']
        for selects in self.fields:
            self.fields[selects].widget.attrs['form'] = 'form-general'

        self.fields['commission_value'].widget.attrs['readonly'] = 'true'
        self.fields['commission_value'].widget.attrs['class']+= ' bg-gray-200' # si se quiere usar atributos extra sin alterar lo que ya esta se debe hacer asi, con el update no se puede

        region_data = {
            'hx-get': '/properties/commune-select',
            'hx-trigger' : 'change delay:500ms',
            'hx-target' : '#communes',
        }
        self.fields['region'].widget.attrs.update(region_data)

        self.fields['video_url'].widget.attrs['class'] = 'focus:outline-none border border-gray-300 rounded-r-lg py-2 px-4 block w-full appearance-none leading-normal text-gray-700'

        # self.fields['commune'].initial = commune
        # self.fields['commune'].widget.attrs['class'] += ' bg-gray-200'
        # self.fields['commune'].widget.attrs['disabled'] = '{% if disabled %}true{% else %}false{% endif %}'


    # more_images = forms.FileField(required=True, label='Mas Imagenes',widget=forms.ClearableFileInput(attrs={
    #     'multiple': True,
    #     'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'
    # }))


    def has_class_attr(self):
        # Check if the title field widget has a class attr
        for field in self.fields:
            if 'class' in self.fields[field].widget.attrs:
                print(field)
        return False


    class Meta:
        model = Property
        fields = (
            # 'state', # debe estar en fields para poder asignarle valor
            'property_type',
            'publish_type',
            'title',
            'description',
            'type_price',
            'price',
            'google_url',
            'video_url',
            'is_featured',
            'is_new',
            'is_iva',
            'region',
            'commune',
            'street_address',
            'realtor',
            'owner',
            'appraisal_value',
            'commission_percentage',
            'commission_value'
        )
        # widgets ={
        #     'commune': forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
        #     'google_url': forms.TextInput(attrs={'placeholder': 'copiar enlace de incorporacion de mapa'}),
        # }

    # def clean_street_address(self):
    #     street_address = self.cleaned_data['street_address']
    #     if len(street_address) < 100:
    #         raise forms.ValidationError('Muy pocos parametros') 
    #     return street_address


    # def clean_price(self):
    #     price = self.cleaned_data['price']
    #     if price <= 0:
    #         msg = 'Precio debe ser mayor a cero'
    #         raise forms.ValidationError(msg) 
    #     return price


    def clean(self):
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        price = cleaned_data.get('price')

        if title is not None:
            cleaned_data['title'] = title.capitalize()
        if price is not None and int(price) <= 0:
            msg = 'Precio debe ser mayor a cero'
            self.add_error('price', msg)
        return cleaned_data

class HouseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['land_surface'].validators = [RegexValidator(r'^[0-9]*$', message='Solo numeros son permitidos')]
        for field in self.fields:
            if field != 'distribution' and field != 'service' and field != 'kitchen' and field != 'other':
                self.fields[field].widget.attrs['class'] = attrs_class
            if self.errors.get(field):
                self.fields[field].widget.attrs['class'] = attrs_class_error

    # VALIDATIONS
    # la "r" significa que la cadena string sera tratada como un "raw string" lo no procesara las combinaciones especiales con backslash "\" 
    # land_surface = forms.IntegerField(label='Superficie de terreno', validators=[RegexValidator(r'^[0-9]*$', message='Solo numeros son permitidos')], required=False)
    class Meta:
        model = House
        fields = (
            'property',
            'land_surface',
            'builded_surface',
            'num_rooms',
            'num_bathrooms',
            'num_parkings',
            'num_cellars',
            'num_floors',
            'num_house',
            'builded_year',
            'common_expenses',
            'distribution',
            'service',
            'kitchen',
            'other'
        )

    def clean(self):
        cleaned_data = self.cleaned_data
        builded_year = cleaned_data.get('builded_year')
        builded_surface = cleaned_data.get('builded_surface')
        land_surface = cleaned_data.get('land_surface')
        if builded_year is not None and builded_year > date.today().year:
            msg = 'El año de construcción debe ser igual o inferior al actual'
            self.add_error('builded_year', msg)
        if builded_surface is not None and builded_surface <= 0:
            msg = 'Superficie construida debe ser mayor a cero'
            self.add_error('builded_surface', msg)
        if land_surface is not None and land_surface <= 0:
            msg = 'Superficie de terreno debe ser mayor a cero'
            self.add_error('land_surface', msg)

class ApartmentForm(forms.ModelForm):
    builded_surface = forms.CharField(label='Superficie construida', validators=[RegexValidator(r'^[0-9]*$', message='Solo numeros son permitidos')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'distribution' and field != 'service' and field != 'kitchen' and field != 'other':
                self.fields[field].widget.attrs['class'] = attrs_class
            if self.errors.get(field):
                self.fields[field].widget.attrs['class'] = attrs_class_error

    class Meta:
        model = Apartment
        fields = (
            'property',
            'land_surface',
            'builded_surface',
            'num_rooms',
            'num_bathrooms',
            'num_parkings',
            'num_apartment',
            'builded_year',
            'common_expenses',
            'distribution',
            'service',
            'kitchen',
            'other'
        )


    def clean_builded_year(self):
        builded_year = self.cleaned_data['builded_year']
        if builded_year:
            if builded_year > date.today().year:
                msg = 'El año de construcción debe ser igual o inferior al actual'
                raise forms.ValidationError(_(msg), code='invalid') # buena practica el "_" para habilitar la traducción y el code para indicar info extra, no es obligatorio usarlo
            return builded_year

    def clean_builded_surface(self):
        builded_surface = self.cleaned_data['builded_surface']
        if builded_surface:
            if int(builded_surface) <= 0:
                msg = 'Superficie construida debe ser mayor a cero'
                msg2 = 'Ponlo bien ahora'
                raise forms.ValidationError([forms.ValidationError(msg), forms.ValidationError(msg2)]) # para mostrar mas de un error a la vez en ese input
        return builded_surface

    def clean_land_surface(self):
        land_surface = self.cleaned_data['land_surface']
        if land_surface:
            if land_surface <= 0:
                msg = 'Superficie de terreno debe ser mayor a cero'
                raise forms.ValidationError(msg) 
        return land_surface

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
        
class RealtorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = attrs_class
            if self.errors.get(field):
                self.fields[field].widget.attrs['class'] = attrs_class_error
    
    class Meta:
        model = Realtor
        fields = ('first_name', 'last_name', 'phone1', 'email')

class OwnerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = attrs_class

            if self.errors.get(field):
                self.fields[field].widget.attrs['class'] = attrs_class_error

        data = {
            'x-mask': '99.999.999-*',
            'placeholder': '99.999.999-9',
        }
        self.fields['rut'].widget.attrs.update(data)
        self.fields['rut'].widget.attrs['class'] += ' uppercase' 

    class Meta:
        model = Owner
        fields = ('name', 'rut', 'phone1', 'email')
        # widgets = {
        #     'rut': forms.TextInput(attrs={
        #         'x-mask': 'aa-99',
        #     })
        # }