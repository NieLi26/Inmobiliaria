from django.urls import path
from .views import ( property_create, property_select, house_list, apartement_list, commune_select, property_delete, property_update,
 property_detail, property_custom_list, custom_status, custom_table, custom_list
    )

urlpatterns = [
    path('panel/publicaciones/', property_custom_list, name='property_custom'),
    path('house/', house_list, name='house_list'),
    path('apartment/', apartement_list, name='apartment_list'),
    path('<str:publish_type>/<str:property_type>/<str:location_slug>/<slug:slug>/<uuid:uuid>/', property_detail, name='property_detail'),
    path('create/<str:property_type>/', property_create, name='property_create'),
    path('select/', property_select, name='property_select'),
    #### testing ####
    path('<str:publish_type>/<str:property_type>/<str:location_slug>/', custom_list, name='custom_list'),
]

hxpatterns = [
    path('delete/<uuid:uuid>/<int:page_number>/', property_delete, name='property_delete'),
    path('update/<str:property_type>/<str:region>/<slug:slug>/<uuid:uuid>/', property_update, name='property_update'),
    path('commune_select/', commune_select, name='commune_select'),
    path('custom_status/<int:pk>/<str:action>/<str:page_number>/', custom_status, name='custom_status'),
    path('custom_table/<int:page_number>/', custom_table, name='custom_table'),
]

urlpatterns += hxpatterns