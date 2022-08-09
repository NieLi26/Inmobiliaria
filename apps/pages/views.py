from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, View
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.conf import settings
from django.core.paginator import Paginator

from .forms import ContactForm
from .models import Contact
from apps.properties.models import House, Apartment

# Create your views here.

class HomePageView(View):
    def get(self, request, *args, **kwargs):
        houses = House.objects.filter(state=True, publish_type='ar')[0:20]
        apartments = Apartment.objects.filter(state=True, publish_type='ve')[0:20]
        context = {
           'house_list': houses,
           'apartment_list': apartments,
        }
        return render(request, 'pages/home.html', context)

class ContactPageView(View):
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form
        }
        return render(request, 'pages/contact.html', context)
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST or None)
        if form.is_valid():
            form.save()
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = 'Su correo ha sido recibido satisfactoriamente lo contactaremos a la brevedad'
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [from_email])
                messages.success(request, "Mensaje enviado correctamente")
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('contact')
        return render(request, 'pages/contact.html')

class ConctactListView(View):
    def get(self, request, *args, **kwargs):
        contact_list = ContactForm.Meta.model.objects.all()
        paginator = Paginator(contact_list, 10)
        page_number = request.GET.get('page')
        properties_data = paginator.get_page(page_number)
        context = {
            'contact_list': properties_data,
            'page_obj': properties_data,
        }
        return render(request, 'pages/contact_list.html', context) 
    
    def post(self, request, *args, **kwargs):
        id = request.POST['contact_id']
        contact = Contact.objects.get(id=id)
        contact.state = False
        contact.save()
        return redirect('contact_list')


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