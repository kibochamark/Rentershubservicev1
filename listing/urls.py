from django.urls import path

from listing.views import PropertyGenericView, PropertyTypeGenericView, PropertyAmmenityGenericView, \
    UpdatePropertyTypeGeneric, CreateListProperties, PropertyFeatureGenericView, UpdatePropertyFeatureGeneric, \
    TestGenericView

urlpatterns=[
    path('property', CreateListProperties.as_view(), name="properties"),
    path('test', TestGenericView.as_view(), name="propert"),
    path('propertytype', PropertyTypeGenericView.as_view(), name="propertytype"),
    path('propertytype/<int:id>/', UpdatePropertyTypeGeneric.as_view(), name="propertytypeupdate"),
    path('propertyfeature', PropertyFeatureGenericView.as_view(), name="propertyfeature"),
    path('propertyfeature/<int:id>/', UpdatePropertyFeatureGeneric.as_view(), name="propertyfeatureupdate"),
    path('propertyamenity', PropertyAmmenityGenericView.as_view(), name="propertyamenityview"),
    path('propertyamenity/<int:id>/', UpdatePropertyTypeGeneric.as_view(), name="propertyamenityviewupdate"),


]