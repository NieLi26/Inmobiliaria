from tkinter.tix import Form
from django import forms

from .models import House, Location, Apartment

class LocationForm(forms.ModelForm):
    
    class Meta:
        model = Location
        exclude = ("state",)


class HouseForm(forms.ModelForm):
    more_images = forms.FileField(required=False, label='Mas Imagenes',widget=forms.FileInput(attrs={
        'multiple': True,
    }))
    class Meta:
        model = House
        exclude = ("state", 'service', 'num_parkings', 'num_cellars', 'num_floors', 'builded_year', 'orientation')
        # widgets ={
        #     'address': forms.TextInput(attrs={'placeholder': 'Ingrese Dirección de Propiedad...'}),
        #     'title': forms.TextInput(attrs={'placeholder': 'Ingrese Titulo para Propiedad...'}),
        #     # 'state': forms.CheckboxInput(attrs={'style': 'width: 5%'}),
        #     'content': forms.Textarea()
        # }

class ApartmentForm(forms.ModelForm):
    more_images = forms.FileField(required=False, label='Mas Imagenes',widget=forms.FileInput(attrs={
        'multiple': True,
    }))
    class Meta:
        model = Apartment
        exclude = ("state",)
        # widgets ={
        #     'address': forms.TextInput(attrs={'placeholder': 'Ingrese Dirección de Propiedad...'}),
        #     'title': forms.TextInput(attrs={'placeholder': 'Ingrese Titulo para Propiedad...'}),
        #     # 'state': forms.CheckboxInput(attrs={'style': 'width: 5%'}),
        #     'content': forms.Textarea()
        # }