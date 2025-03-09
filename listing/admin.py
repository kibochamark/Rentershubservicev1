from django.contrib import admin

from listing.models import Connections, Property, PropertyType, PropertyFeature, Revenue, Unit, SpaceType, UnitImage, PropertyAmenity, TestGis

# Register your models here.
admin.site.register(Property)
admin.site.register(SpaceType)
admin.site.register(UnitImage)
admin.site.register(Unit)
admin.site.register(PropertyType),
admin.site.register(PropertyFeature)
admin.site.register(PropertyAmenity)
admin.site.register(TestGis)
admin.site.register(Connections)
admin.site.register(Revenue)