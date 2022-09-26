from ast import Try
from multiprocessing import context
from xml.dom import ValidationErr
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, View
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
#cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from .forms import ContactForm
from .models import Contact
from apps.properties.models import House, Apartment

# Create your views here.

class HomePageView(View):
    def get(self, request, *args, **kwargs):
        houses = House.objects.filter(state=True, property__publish_type='ve')[0:20]
        apartments = Apartment.objects.filter(state=True, property__publish_type='ve')[0:20]
        context = {
           'house_list': houses,
           'apartment_list': apartments,
        }
        return render(request, 'pages/home.html', context)

@method_decorator(never_cache, name='dispatch')
class ContactPageView(SuccessMessageMixin, View):
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form
        }
        return render(request, 'pages/contact.html', context)
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mensaje enviado correctamente")    
            return redirect('contact')
        return render(request, 'pages/contact.html', {'form': form})

    def get_success_message(self, cleaned_data) -> str:
        return super().get_success_message(cleaned_data)


class ConctactListView(View):
    def get(self, request, *args, **kwargs):
        contact_list = ContactForm.Meta.model.objects.all()
        paginator = Paginator(contact_list, 5)
        page_number = request.GET.get('page')
        properties_data = paginator.get_page(page_number)
        context = {
            # 'contact_list': properties_data,
            'page_obj': properties_data,
        }
        return render(request, 'pages/contact_list.html', context) 
    
    # def post(self, request, *args, **kwargs):
    #     q = request.POST.get('q', '')
    #     page_number = request.POST.get('page_number', '')
    #     contact_list = Contact.objects.filter(name__icontains=q)
    #     paginator = Paginator(contact_list, 5)
    #     # page_number = request.GET.get('page')
    #     properties_data = paginator.get_page(page_number)
    #     context = {
    #         # 'contact_list': properties_data,
    #         'page_obj': properties_data,
    #     }
    #     return render(request, 'partials/contact_table.html', context) 

def hx_contact_table(request, page_number):
    q = request.POST.get('q', '')
    print(q)
    contact_list = Contact.objects.filter(name__icontains=q)
    paginator = Paginator(contact_list, 5)
    properties_data = paginator.get_page(page_number)
    context = {
        # 'contact_list': properties_data,
        'page_obj': properties_data,
    }
    return render(request, 'partials/contact_table.html', context) 

def hx_contact_modal(request, pk, page_number):
    contact = Contact.objects.get(id=pk)
    contact.state = False
    contact.save()
    contact_list = ContactForm.Meta.model.objects.all()
    paginator = Paginator(contact_list, 5)
    properties_data = paginator.get_page(page_number)
    context = {
        'page_obj': properties_data,
    }
    response = render(request, 'partials/contact_table.html', context)
    response['HX-Trigger'] = 'modal-contact-button' # pasamos un encabezado para activar el trigger
    return response

def hx_contact_notify(request):
    return render(request, 'partials/contact_notify.html')

# def hx_message(request):
#     return render(request, 'partials/contact_alerts.html')


# class ContactPageView(FormView):
#     template_name = 'pages/contact.html'
#     form_class = ContactForm
#     success_url = reverse_lazy('contact')

#     def form_valid(self, form):
#         subject = form.cleaned_data['subject']
#         # name = form.cleaned_data['name']
#         # phone = form.cleaned_data['phone']
#         from_email = form.cleaned_data['from_email']
#         message = form.cleaned_data['message']
#         try:
#             send_mail(subject, message, from_email, ['seba.diamond5@gmail.com'])
#         except BadHeaderError:
#             return HttpResponse('Invalid header found.')
#         return super().form_valid(form)

    

# def contactView(request):
#     if request.method == 'GET':
#         form = ContactForm()
#     else:
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data['subject']
#             from_email = form.cleaned_data['from_email']
#             message = form.cleaned_data['message']
#             try:
#                 send_mail(subject, message, from_email, ['admin@example.com'])
#             except BadHeaderError:
#                 return HttpResponse('Invalid header found.')
#             return redirect('success')
#     return render(request, "email.html", {'form': form})

# def successView(request):
#     return HttpResponse('Success! Thank you for your message.')




###################### fomr with htmx falta limpiar cache ################

# class ContactPageView(SuccessMessageMixin, View):
#     def get(self, request, *args, **kwargs):
#         form = ContactForm()
#         context = {
#             'form': form
#         }
#         return render(request, 'pages/contact.html', context)
#         # response = render(request, 'pages/contact.html', context)
#         # response['HX-Trigger'] = 'message-form'
#         # return response
    
#     def post(self, request, *args, **kwargs):
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # messages.success(request, "Mensaje enviado correctamente")  
#             response = render(request, 'partials/contact_form.html', {'form': ContactForm()})
#             response['HX-Trigger'] = 'modal-contact-button' 
#             return response
#         return render(request, 'partials/contact_form.html', {'form': form})


####################### mensaje en signals ##########################
# class ContactPageView(SuccessMessageMixin, View):
#     def get(self, request, *args, **kwargs):
#         form = ContactForm()
#         context = {
#             'form': form
#         }
#         return render(request, 'pages/contact.html', context)
    
#     def post(self, request, *args, **kwargs):
#         form = ContactForm(request.POST or None)
#         if form.is_valid():
#             form.save()
#             subject = form.cleaned_data['subject']
#             from_email = form.cleaned_data['from_email']
#             message = 'Su correo ha sido recibido satisfactoriamente lo contactaremos a la brevedad'
#             try:
#                 send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [from_email])
#                 messages.success(request, "Mensaje enviado correctamente")    
#                 return redirect('contact')
#             except BadHeaderError:
#                 return HttpResponse('Invalid header found.')
#         return render(request, 'pages/contact.html', {'form': form})