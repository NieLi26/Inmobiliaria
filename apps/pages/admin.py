from django.contrib import admin

from .models import Contact
# Register your models here.

# class PropertyAdmin(admin.ModelAdmin):
#     list_display = ("property_type", "publish_type", "price", 'uf')

admin.site.register(Contact)
