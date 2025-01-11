from django.contrib import admin

from listing.models import Property, PropertyType, Unit, SpaceType, UnitImage, PropertyAmenity

# Register your models here.
admin.site.register(Property)
admin.site.register(SpaceType)
admin.site.register(UnitImage)
admin.site.register(Unit)
admin.site.register(PropertyType)
admin.site.register(PropertyAmenity)