from django.urls import path
from .views import LocationCreateView, DescriptionCreateView, HouseListView, HouseDetailView, ApartmentListView, ApartmentDetailView, PropertyCustomListView

urlpatterns = [
    path('panel/publicaciones/', PropertyCustomListView.as_view(), name='property_custom'),
    path('publicar/ubicacion/', LocationCreateView.as_view(), name='location_create'),
    path('publicar/description/<uuid:uuid>/', DescriptionCreateView.as_view(), name='description_create'),
    # path('', PropertyListView.as_view(), name='property_list'),
    path('house/', HouseListView.as_view(), name='house_list'),
    path('house/<uuid:uuid>/', HouseDetailView.as_view(), name='house_detail'),
    path('apartment/', ApartmentListView.as_view(), name='apartment_list'),
    path('apartment/<uuid:uuid>/', ApartmentDetailView.as_view(), name='apartment_detail'),


    # path('apartment/', PropertyApartmentListView.as_view(), name='property_apartment_list'),
    # path('custom/', PropertyCustomListView.as_view(), name='property_custom'),
    # path('<uuid:uuid>/', PropertyDetailView.as_view(), name='property_detail'),
    # path('<uuid:uuid>/edit/', PropertyUpdateView.as_view(), name='property_edit'),
    # path('delete/', PropertyDeleteView.as_view(), name='property_delete'),
    # path('create/', PropertyCreateView.as_view(), name='property_create'),
]