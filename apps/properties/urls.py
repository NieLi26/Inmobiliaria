from django.urls import path
from . import views

app_name = "properties"

urlpatterns = [
    # LIST 
    path('panel/publicaciones/', views.property_publish_list, name='property_custom'), # publish
    path('panel/despublicaciones/', views.PropertyDraftListView.as_view(), name='property_custom_draft'), #draft
    # DETAIL
    path('<str:publish_type>/<str:property_type>/<str:location_slug>/<slug:slug>/<uuid:uuid>/', views.property_detail, name='property_detail'),
    # CREATE
    path('create/<str:property_type>/', views.property_create, name='property_create'),
    # UPDATE
    path('update/<slug:slug>/<uuid:uuid>/', views.property_update, name='property_update'),

    path('select/', views.property_select, name='property_select'),
    
    # GALERY
    path('galery/<slug:slug>/<uuid:uuid>/', views.PropertyGaleryView.as_view(), name='property_galery'),

    # CONTACT LIST
    path('panel/contacts/', views.PropertyContactListView.as_view(), name='contact_list'),

    #### testing ####
    path('<str:publish_type>/<str:property_type>/<str:location_slug>/', views.custom_list, name='custom_list'),
    path('<str:first_data>/<str:second_data>/', views.custom_list_publish_property, name='custom_list_publish_property'),
    # path('<str:publish_type>/<str:location_slug>/', custom_list_publish_location, name='custom_list_publish_location'),
    path('<str:publish_type>/', views.custom_list_publish, name='custom_list_publish'),

    #1
    path('property_list/<int:page_number>/<str:publish_type>/<str:property_type>/<str:location_slug>', views.property_list, name='property_list'),
    #2
    path('property_list_publish_property/<int:page_number>/<str:first_data>/<str:second_data>', views.property_list_publish_property, name='property_list_publish_property'),
    #3
    path('property_list_publish/<int:page_number>/<str:publish_type>', views.property_list_publish, name='property_list_publish'),

    
]

hxpatterns = [
    # LIST PUBLISH
    path('delete/<uuid:uuid>/<int:page_number>/', views.property_delete, name='custom_delete'),
    path('custom_status/<int:pk>/<str:action>/<str:page_number>/', views.custom_status, name='custom_status'),
    path('custom_featured/<int:pk>/<str:action>/<str:page_number>/', views.custom_featured, name='custom_featured'),
    path('custom_table/<int:page_number>', views.custom_table, name='custom_table'),
    # LIST DRAFT
    path('delete/<uuid:uuid>/<int:page_number>/draft/', views.PropertyDeleteView.as_view(), name='property_delete'),
    path('custom_status/<int:pk>/<str:action>/<str:page_number>/draft/', views.PropertyStatusView.as_view(), name='property_status'),
    path('custom_featured/<int:pk>/<str:action>/<str:page_number>/draft/', views.PropertyFeaturedView.as_view(), name='property_featured'),
    path('custom_table/<int:page_number>/draft', views.TableDraftView.as_view(), name='table_draft'),
    # CREATE AND UPDATE
    path('commune_select', views.commune_select, name='commune_select'),
    # DETAIL
    path('contact_detail_form/<str:publish_type>/<str:property_type>/<str:location_slug>/<slug:slug>/<uuid:uuid>/', views.contact_detail_form, name='contact_detail_form'),

    # CONTACT LIST
    path('table_contact/<int:page_number>', views.TableContactView.as_view(), name='table_contact'),
    path('modal_contact/<int:pk>/<int:page_number>', views.ModalContactView.as_view(), name='modal_contact'),
]

urlpatterns += hxpatterns