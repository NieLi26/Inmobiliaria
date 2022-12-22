from django.urls import path
from . import views

app_name = "properties"

urlpatterns = [
    ## PANEL
    path('panel/publicaciones/', views.property_publish_list, name='property_custom_publish'), 
    path('panel/despublicaciones/', views.DraftListView.as_view(), name='property_custom_draft'), 
    path('panel/contacts/', views.PropertyContactListView.as_view(), name='contact_property_list'),

    ## REALTOR
    path('realtor/', views.RealtorListView.as_view(), name='realtor_list'),
    path('realtor/create/', views.RealtorCreateView.as_view(), name='realtor_create'),
    path('realtor/<int:pk>/detail/', views.RealtorDetailView.as_view(), name='realtor_detail'),
    path('realtor/<int:pk>/update/', views.RealtorUpdateView.as_view(), name='realtor_update'),

    ## PROPERTY
    path('<str:publish_type>/<str:property_type>/<str:location_slug>/<slug:slug>/<uuid:uuid>/', views.property_detail, name='property_detail'),
    path('<str:property_type>/create/', views.property_create, name='property_create'),
    path('<slug:slug>/<uuid:uuid>/update/', views.property_update, name='property_update'),
    path('select/', views.property_select, name='property_select'),
    
    ## GALERY
    path('galery/<slug:slug>/<uuid:uuid>/', views.PropertyGaleryView.as_view(), name='property_galery'),

    ## RESULTADOS 
    path('<str:publish_type>/<str:property_type>/<str:location_slug>/', views.custom_list, name='custom_list'),
    path('<str:first_data>/<str:second_data>/', views.custom_list_publish_property, name='custom_list_publish_property'),
    path('<str:publish_type>/', views.custom_list_publish, name='custom_list_publish'),

    #1
    path('property_list/<int:page_number>/<str:publish_type>/<str:property_type>/<str:location_slug>', views.property_list, name='property_list'),
    #2
    path('property_list_publish_property/<int:page_number>/<str:first_data>/<str:second_data>', views.property_list_publish_property, name='property_list_publish_property'),
    #3
    path('property_list_publish/<int:page_number>/<str:publish_type>', views.property_list_publish, name='property_list_publish'),

    
]

hxpatterns = [
    ## PUBLISH
    path('publish/<uuid:uuid>/<int:page_number>/delete', views.publish_delete, name='publish_delete'),
    path('publish/<int:pk>/<str:action>/<str:page_number>/status', views.publish_status, name='publish_status'),
    path('publish/<int:pk>/<str:action>/<str:page_number>/fatured', views.publish_featured, name='publish_featured'),
    path('publish/<int:page_number>/table', views.table_publish, name='table_publish'),

    ## DRAFT
    path('draft/<uuid:uuid>/<int:page_number>/delete/', views.DraftDeleteView.as_view(), name='draft_delete'),
    path('draft/<int:pk>/<str:action>/<str:page_number>/status/', views.DraftStatusView.as_view(), name='draft_status'),
    path('draft/<int:pk>/<str:action>/<str:page_number>/featured/', views.DraftFeaturedView.as_view(), name='draft_featured'),
    path('draft/<int:page_number>/table', views.TableDraftView.as_view(), name='table_draft'),

    ## CREATE AND UPDATE
    path('commune_select', views.commune_select, name='commune_select'),

    ## DETAIL
    path('contact_detail_form/<str:publish_type>/<str:property_type>/<str:location_slug>/<slug:slug>/<uuid:uuid>/', views.contact_detail_form, name='contact_detail_form'),

    ## CONTACT 
    path('contact/table_contact/<int:page_number>/table', views.TableContactView.as_view(), name='table_contact'),
    path('contact/modal_contact/<int:pk>/<int:page_number>/modal', views.ModalContactView.as_view(), name='modal_contact'),

    ## REALTOR 
    path('realtor/<int:page_number>/table', views.TableRealtorView.as_view(), name='table_realtor'),
    path('realtor/<int:pk>/<int:page_number>/realtor/delete/', views.RealtorDeleteView.as_view(), name='realtor_delete'),
]

urlpatterns += hxpatterns