from django.urls import path
from .views import HomePageView, ContactPageView, ConctactListView, hx_contact_modal, hx_contact_notify, hx_contact_table

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('contact/list/', ConctactListView.as_view(), name='contact_list'),
]


hxpatterns = [
    path('hx_contact_modal/<int:pk>/<int:page_number>/', hx_contact_modal, name='hx_contact_modal'),
    path('hx_contact_notify/', hx_contact_notify, name='hx_contact_notify'),
    path('hx_contact_table/<int:page_number>/', hx_contact_table, name='hx_contact_table'),
    # path('hx_message/', hx_message, name='hx_message'),
]

urlpatterns += hxpatterns