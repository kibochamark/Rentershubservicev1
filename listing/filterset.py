import django_filters

from listing.models import Property


class PropertyFilter(django_filters.FilterSet):
    rent_price=django_filters.RangeFilter(field_name="rent_price")
    propertytype_name=django_filters.CharFilter(field_name="property_type__name", lookup_expr="icontains")
    condition_name=django_filters.CharFilter(field_name="features__name", lookup_expr="icontains")
    managed_by=django_filters.CharFilter(field_name="managed_by", lookup_expr="icontains")
    is_approved=django_filters.BooleanFilter(field_name="is_approved")

    class Meta:
        model = Property
        fields =['rent_price', 'propertytype_name', 'managed_by', 'is_approved', 'condition_name']