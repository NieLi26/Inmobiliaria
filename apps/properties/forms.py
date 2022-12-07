import re
from django import forms


from .models import House, Property, Apartment, Commune, Region, PropertyContact
class PropertyForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['autocomplete'] = "off"

        

    # more_images = forms.FileField(required=True, label='Mas Imagenes',widget=forms.ClearableFileInput(attrs={
    #     'multiple': True,
    #     'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'
    # }))

    class Meta:
        model = Property
        exclude = ('state', 'slug',)
        widgets ={
            # General
            'property_type': forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm', 'style': 'display:none'}),
            'publish_type': forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'land_surface': forms.NumberInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md', "min": 0,'value':0}),
            'title': forms.TextInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'description': forms.Textarea(attrs={'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 mt-1 block w-full sm:text-sm border border-gray-300 rounded-md'}),
            'type_price': forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'price': forms.NumberInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md', "min": 0,'value':0}),

            # Ubicación
            # 'region': forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm', 'hx-get': "'{% url 'commune_select' %}'", 'hx-trigger': 'change delay:500ms', 'hx-target': '#communes'}),
            'region': forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm', "hx-get": "/properties/commune_select", 'hx-trigger': 'change delay:500ms', 'hx-target': '#communes'}),
            'commune': forms.Select(attrs={'class': 'mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}),
            'street_address': forms.TextInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            'street_number': forms.TextInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            
            # url directions
            'google_url': forms.TextInput(attrs={'class': 'block w-full flex-1 rounded-none rounded-r-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),
            'video_url': forms.TextInput(attrs={'class': 'block w-full flex-1 rounded-none rounded-r-md border-gray-300 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm'}),

            'is_featured': forms.CheckboxInput(attrs={'class': 'focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded'}),

            # Contact
            'phone1': forms.TextInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md', 'placeholder':'Ej. 945643233'}),
            'phone2': forms.TextInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md', 'placeholder':'Ej. 945643233'}),
        
            # imagen
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'})
        }

    # def save(self, commit=True):
    #     print(self.cleaned_data)
    #     property = super().save(commit)
    #     print(property.more.images)
    #     return property

    # def clean_commune(self):
    #     communes = Commune.objects.values_list('name', flat=True)
    #     commune = self.cleaned_data['commune']
    #     for c in communes:
    #         if c == commune:
    #             raise forms.ValidationError('Debe escojer una comuna dentro del listado')
    #     return commune

    # def clean_region(self):
    #     regions = Region.objects.values_list('name', flat=True)
    #     region = self.cleaned_data['region']
    #     for r in regions:
    #         if r == region:
    #             raise forms.ValidationError('Debe escojer una region dentro del listado')
    #     return region

    # def clean_street_address(self):
    #     street_address = self.cleaned_data['street_address']
    #     if len(street_address) < 100:
    #         raise forms.ValidationError('Muy pocos parametros') 
    #     return street_address

    def clean_land_surface(self):
        land_surface = self.cleaned_data['land_surface']
        if land_surface == 4:
            raise forms.ValidationError('Muy pocos parametros') 
        return land_surface

class HouseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'is_furnished':
                self.fields[field].widget.attrs["class"] = "focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
            else:
                self.fields[field].widget.attrs["class"] = "mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
    class Meta:
        model = House
        exclude = ("state", "property")
        widgets ={
            # 'builded_surface': forms.NumberInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md', "min": 0,'value':0}),
            # 'num_rooms': forms.NumberInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md', "min": 0,'value':0}),
            # 'num_bathrooms': forms.NumberInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md', "min": 0,'value':0}),
            # 'num_parkings': forms.NumberInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md', "min": 0,'value':0}),
            # 'num_cellars': forms.NumberInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md', "min": 0,'value':0}),
            # 'num_floors': forms.NumberInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md', "min": 0,'value':0}),
            # 'builded_year': forms.NumberInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md', "min": 0,'value':0}),
            # 'floor_type': forms.TextInput(attrs={'class': 'mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md'}),
            # 'is_furnished': forms.CheckboxInput(attrs={'class': 'focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded'}),
        }

class ApartmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'is_furnished':
                self.fields[field].widget.attrs["class"] = "focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded"
            else:
                self.fields[field].widget.attrs["class"] = "mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
    class Meta:
        model = Apartment
        exclude = ("state", "property")

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