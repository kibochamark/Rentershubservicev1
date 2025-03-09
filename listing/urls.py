from django.urls import path

from listing.views import PropertyGenericView, PropertyTypeGenericView, PropertyAmmenityGenericView, RevenueGeneric, RevenueUpdateDelete, SummaryViewSet, \
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

    path('revenue', RevenueGeneric.as_view(), name="revenue"),
    path('revenue/<int:id>/', RevenueUpdateDelete.as_view(), name="revenueviewupdate"),


    path('<int:user_id>/getsummarybylandlordorgroundagent/', SummaryViewSet.as_view({
        'get':'get_tenant_groundagent_summary'
    })),

    path('adminsummary', SummaryViewSet.as_view({
        'get':'get_admin_summary'
    }))

]