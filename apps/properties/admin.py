from django.contrib import admin
from .models import House, HouseImage, Location, Apartment, ApartmentImage

# Register your models here.
class HouseImageInline(admin.TabularInline):
    model = HouseImage


class HouseAdmin(admin.ModelAdmin):
    inlines = [
        HouseImageInline,
    ]
    list_display = ("title", "location" ,"publish_type", "type_price", 'price')

class ApartmentImageInline(admin.TabularInline):
    model = ApartmentImage


class ApartmentAdmin(admin.ModelAdmin):
    inlines = [
        ApartmentImageInline,
    ]
    list_display = ("title", 'location', "publish_type", "type_price", 'price')

admin.site.register(House, HouseAdmin)
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Location)
