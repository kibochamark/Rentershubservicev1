from django.urls import path

from listing.views import PropertyGenericView, PropertyTypeGenericView, PropertyAmmenityGenericView, \
    UpdatePropertyTypeGeneric, CreateListProperties, PropertyFeatureGenericView, UpdatePropertyFeatureGeneric, \
    UpdatePropertyGeneric, Spacetypesgeneric, UpdateSpaceTypeGeneric, Unitgeneric, UpdateUnitGeneric

urlpatterns=[
    path('property', CreateListProperties.as_view(), name="properties"),
    path('property/<int:id>/', UpdatePropertyGeneric.as_view(), name="propertyupdate"),
    path('propertytype', PropertyTypeGenericView.as_view(), name="propertytype"),
    path('propertytype/<int:id>/', UpdatePropertyTypeGeneric.as_view(), name="propertytypeupdate"),
    path('propertyfeature', PropertyFeatureGenericView.as_view(), name="propertyfeature"),
    path('propertyfeature/<int:id>/', UpdatePropertyFeatureGeneric.as_view(), name="propertyfeatureupdate"),
    path('propertyamenity', PropertyAmmenityGenericView.as_view(), name="propertyamenityview"),
    path('propertyamenity/<int:id>/', UpdatePropertyTypeGeneric.as_view(), name="propertyamenityviewupdate"),

    path('spacetype', Spacetypesgeneric.as_view(), name="spacetypeview"),
    path('spacetype/<int:id>/', UpdateSpaceTypeGeneric.as_view(), name="spacetypeviewupdate"),

    path('unit', Unitgeneric.as_view(), name="unitview"),
    path('unit/<int:id>/', UpdateUnitGeneric.as_view(), name="updateunitviewupdate"),

]