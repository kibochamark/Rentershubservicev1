import django_filters

from listing.models import Property


class PropertyFilter(django_filters.FilterSet):
    rent_price=django_filters.RangeFilter(field_name="rent_price")
    propertytype_name=django_filters.CharFilter(field_name="property_type__name", lookup_expr="icontains")
    managed_by=django_filters.CharFilter(field_name="managed_by", lookup_expr="icontains")

    class Meta:
        model = Property
        fields =['rent_price', 'propertytype_name', 'managed_by']