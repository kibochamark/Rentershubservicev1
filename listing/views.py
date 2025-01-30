from http import HTTPStatus

import geocoder
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from accounts.models import RentersUser
from accounts.permissions import IsApprovedPermissions
from accounts.util import get_geocode
from listing.models import Property, PropertyType, PropertyAmenity, PropertyFeature, TestGis, SpaceType, Unit
from listing.serializers import PropertySerializer, PropertyTypeSerializer, PropertyAmenitySerializer, \
    PropertyFeatureSerializer, SpaceTypeSerializer, UnitSerializer


# Create your views here.



class PropertyGenericView(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
    permission_classes = [permissions.AllowAny]


    def get_queryset(self, *args, **kwargs):
        userid = self.request.GET.get("userid")
        qs = self.queryset
        print(userid)
        if userid:
            newqs = qs.filter(posted_by=int(userid)).all().order_by('title', "-id")
            print(qs)
            return newqs
        return qs


    



    def perform_create(self, serializer):
        address= serializer.initial_data["address"]
        point="Point()"


        if address:
            print(address)
            geo=geocoder.google('Mountain View, CA')
            lat=geo.latlng[0]
            lng=geo.latlng[1]
            point=f"Point({str(lng)} {str(lat)}"

        return serializer.save(location=point)






#property type - get, post, delete and put apis

class PropertyTypeGenericView(generics.ListCreateAPIView):
    queryset = PropertyType.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, permissions.DjangoModelPermissions]
    serializer_class = PropertyTypeSerializer

    lookup_field = 'id'


    def get_queryset(self, *args, **kwargs):
        qs = self.queryset.order_by('name')

        return qs






class UpdatePropertyTypeGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = PropertyType.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, permissions.DjangoModelPermissions]
    serializer_class = PropertyTypeSerializer

    lookup_field = 'id'




#property amenities- get, post, delete and put apis
class PropertyAmmenityGenericView(generics.ListCreateAPIView):
    queryset = PropertyAmenity.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, permissions.DjangoModelPermissions]
    serializer_class = PropertyAmenitySerializer


class UpdatePropertyAmenityGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = PropertyAmenity.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, permissions.DjangoModelPermissions]
    serializer_class = PropertyAmenitySerializer

    lookup_field = 'id'




#property feature - get, post, delete and put apis
class PropertyFeatureGenericView(generics.ListCreateAPIView):
    """get and create property features"""
    queryset = PropertyFeature.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, permissions.DjangoModelPermissions]
    serializer_class = PropertyFeatureSerializer

    def get_queryset(self, *args, **kwargs):
        propertytype = self.request.GET.get("propertytype")
        qs = self.queryset
        if propertytype:
            qs=qs.filter(propertytype=int(propertytype)).all().order_by('name', "-id")
            print(qs)

        return qs


class UpdatePropertyFeatureGeneric(generics.RetrieveUpdateDestroyAPIView):
    """update and delete property features"""
    queryset = PropertyFeature.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, permissions.DjangoModelPermissions]
    serializer_class = PropertyFeatureSerializer

    lookup_field = 'id'




#property apis
class CreateListProperties(generics.ListCreateAPIView):
    """get and create properties"""
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsApprovedPermissions]

    def get_queryset(self, *args, **kwargs):
        userid = self.request.GET.get("userid")
        qs = self.queryset.order_by('updated_at')
        print(userid)
        if userid:
            newqs = qs.filter(posted_by=int(userid)).all().order_by('title', "-id")
            print(qs)
            return newqs
        return qs


    def perform_create(self, serializer):
        address = serializer.initial_data["address"]
        features = serializer.initial_data["features"]
        amenities = serializer.initial_data["amenities"]
        posted_by = serializer.initial_data["posted_by"]



        print(address, features, amenities, posted_by)

        #get geocode from address

        generated_location="Point(-133.72 36)"
        status, data= get_geocode(address)

        #print(generated_location, status, data)

        if status == 200:
            generated_location = f"Point({data['lon']} {data['lat']})"


        feature_set = []
        amenities_set = []

        if not isinstance(features, list) or not isinstance(amenities, list):
            raise ValidationError("features/amenities should be a list")

        for f in features:
            feat = get_object_or_404(PropertyFeature, id=f)
            if feat:
                feature_set.append(feat)

        for a in amenities:
            amen = get_object_or_404(PropertyAmenity, id=a)
            if amen:
                amenities_set.append(amen)




        return serializer.save(location=generated_location, features=feature_set, amenities=amenities_set, posted_by=self.request.user)





class UpdatePropertyGeneric(generics.RetrieveUpdateDestroyAPIView):
    """update and delete property"""
    queryset = Property.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsApprovedPermissions]
    serializer_class = PropertySerializer

    lookup_field = 'id'



class Spacetypesgeneric(generics.ListCreateAPIView):
    """get and create properties"""
    queryset = SpaceType.objects.all()
    serializer_class = SpaceTypeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsApprovedPermissions]




class UpdateSpaceTypeGeneric(generics.RetrieveUpdateDestroyAPIView):
    """update and delete property"""
    queryset = SpaceType.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsApprovedPermissions]
    serializer_class = SpaceTypeSerializer

    lookup_field = 'id'







#unit apis


class Unitgeneric(generics.ListCreateAPIView):
    """get and create unit"""
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsApprovedPermissions]

class UpdateUnitGeneric(generics.RetrieveUpdateDestroyAPIView):
    """update and delete property unit"""
    queryset = Unit.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsApprovedPermissions]
    serializer_class = UnitSerializer

    lookup_field = 'id'
