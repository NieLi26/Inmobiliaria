from django.urls import path
from .views import HomePageView, ContactPageView, ConctactListView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('contact/list/', ConctactListView.as_view(), name='contact_list'),
]