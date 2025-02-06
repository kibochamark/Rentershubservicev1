from django.http.request import RAISE_ERROR
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from listing.models import Property, PropertyFeature, PropertyAmenity, SpaceType, Unit, UnitImage, PropertyType, TestGis


class UnitImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitImage
        fields = ['id', 'image_url', 'alt_text']



class PropertyTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyType
        fields = ['id', 'name', ]



class PropertyFeatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyFeature
        fields = ['id', 'name', 'propertytype']



class PropertyAmenitySerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyAmenity
        fields = ['id', 'name']


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model=Unit
        fields=['id', 'status', 'space_type', 'unit_number']
        read_only=['space_type']


class SpaceTypeSerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True, read_only=True)

    class Meta:
        model = SpaceType
        fields = ['id', 'name', 'property',  'size_in_sqm', 'num_bedrooms', 'num_bathrooms', 'parking_spaces', 'monthly_rent', 'deposit_amount', 'units']


class PropertySerializer(serializers.ModelSerializer):
    space_types = SpaceTypeSerializer(many=True, read_only=True)

    distance= serializers.DecimalField(read_only=True, source='distance.mi', max_digits=10, decimal_places=2, required=False)
    propertytype=PropertyTypeSerializer(source="property_type", read_only=True)
    location_coords = serializers.SerializerMethodField()  # ✅ Link the method




    class Meta:
        model = Property
        fields =[
            'id',
            'distance',
            'title',
            'description',
            'property_type',
            'propertytype',
            'price',
            'city',
            'state',
            'country',
            'postal_code',
            'address',
            'location',
            'location_coords',
            'postal_code',
            'size',
            'bedrooms',
            'bathrooms',
            'parking_spaces',
            'is_available',
            'is_approved',
            'featured',
            'rent_price',
            'deposit_amount',
            'main_image_url',
            'images',
            'features',
            'amenities',
            'water_charges',
            'water_deposit',
            'garbage_charges',
            'security_charges',
            'other_charges',
            'posted_by',
            'managed_by',
            'space_types',
            'updated_at'
        ]

        read_only_fields = ['location', 'is_approved', 'is_available', 'updated_at']


        def get_location_coords(self, obj):
            if obj and obj.location:
                coords = obj.location.coords
                return coords
            return null
        












