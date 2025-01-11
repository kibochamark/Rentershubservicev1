from rest_framework import serializers

from listing.models import Property, PropertyFeature, PropertyAmenity, SpaceType, Unit, UnitImage, PropertyType


class UnitImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitImage
        fields = ['id', 'image_url', 'alt_text']



class PropertyTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyType
        fields = ['id', 'name']



class PropertyFeatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyFeature
        fields = ['id', 'name']



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
        fields = ['id', 'name', 'size_in_sqm', 'num_bedrooms', 'num_bathrooms', 'parking_spaces', 'monthly_rent', 'units']


class PropertySerializer(serializers.ModelSerializer):
    space_types = SpaceTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = ['id', 'title', 'address', 'property_type', 'description', 'space_types']

        read_only_fields = ['location']