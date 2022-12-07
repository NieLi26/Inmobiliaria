import re
from django.forms import TextInput
from django.urls import reverse_lazy
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Contact, OwnerContact

class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # self.helper.form_action = reverse_lazy('home')
        # self.helper.form_id = 'id-exampleForm'
        # self.helper.form_method = 'post'
        # self.helper.form_class = 'blueForms'
        
        # self.helper.add_input(Submit('submit', 'Submit'))
        
    # from_email = forms.EmailField(required=True, label='Correo', widget=forms.TextInput(attrs={'class': 'w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 px-3 leading-8 transition-colors duration-200 ease-in-out'}))
    # subject = forms.CharField(required=True, label='Asunto', widget=forms.TextInput(attrs={'class': 'w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 px-3 leading-8 transition-colors duration-200 ease-in-out'}))
    # name = forms.CharField(required=True, label='Nombre', widget=forms.TextInput(attrs={'class': 'w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 px-3 leading-8 transition-colors duration-200 ease-in-out'}))
    # phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'ej: 934652356', 'class': 'w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 px-3 leading-8 transition-colors duration-200 ease-in-out'}) , required=False, label='Télefono(opcional)')
    # message = forms.CharField(widget=forms.Textarea(attrs={'class':'w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200 h-32 text-base outline-none text-gray-700 py-1 px-3 resize-none leading-6 transition-colors duration-200 ease-in-out'}), required=True, label='Mensaje')
    class Meta:
        model = Contact
        exclude = ('state', )

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        patron = '^[0-9]+$'
        print(re.search(patron, phone))
        if re.search(patron, phone) == None and phone != '' :
            raise forms.ValidationError('Solo debe ingresar numeros')
        return phone
class OwnerContactForm(forms.ModelForm):
    class Meta:
        model = OwnerContact
        exclude = ('state',)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        patron = '^[0-9]+$'
        print(re.search(patron, phone))
        if re.search(patron, phone) == None and phone != '' :
            raise forms.ValidationError('Solo debe ingresar numeros')
        return phone