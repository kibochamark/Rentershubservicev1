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

    #address= serializers.CharField(write_only=True)



    class Meta:
        model = Property
        fields =[
            'title',
            'description',
            'property_type',
            'price',
            'city',
            'state',
            'country',
            'postal_code',
            'address',
            'location',
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
            'posted_by',
            'managed_by',
            'space_types'
        ]

        read_only_fields = ['location', 'is_approved', 'is_available']




        def create(self, validated_data):
            address= validated_data.pop("address")
            location = validated_data.pop("location")
            features = validated_data.po("features")
            amenities = validated_data.pop("amenities")
            posted_by= validated_data.pop("posted_by")

            feature_set=[]
            amenities_set=[]

            if not isinstance(features, list) or not isinstance(amenities, list):
                raise ValidationError("features/amenities should be a list")

            for f in features:
                feat= get_object_or_404(PropertyFeature, id=f)
                if feat:
                    feature_set.append(feat)

            for a in amenities:
                amen=get_object_or_404(PropertyAmenity, id=a)
                if amen:
                    amenities_set.append(amen)

            location="Point(-133.72 36)"


            return Property.objects.create(location=location, posted_by=self.context.get("request").user, amenities=amenities, features=features, **validated_data)





class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model=TestGis
        fields=["location",
                "address"]


        read_only_fields=["location"]



    def create(self, validated_data):
        address= validated_data.pop("address")
        print(address)

        location="Point(-132.24 46)"

        return TestGis.objects.create(location=location,**validated_data)