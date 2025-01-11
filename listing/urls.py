from django.urls import path

from listing.views import PropertyGenericView, PropertyTypeGenericView, PropertyAmmenityGenericView, \
    UpdatePropertyTypeGeneric

urlpatterns=[
    path('properties', PropertyGenericView.as_view(), name="properties"),
    path('propertytype', PropertyTypeGenericView.as_view(), name="propertytype"),
    path('propertytype/<int:id>/', UpdatePropertyTypeGeneric.as_view(), name="propertytypeupdate"),
    path('propertyamenity', PropertyAmmenityGenericView.as_view(), name="propertyamenityview"),
    path('propertyamenity/<int:id>/', UpdatePropertyTypeGeneric.as_view(), name="propertyamenityviewupdate"),

]