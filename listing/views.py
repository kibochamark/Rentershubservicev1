from http import HTTPStatus

import geocoder
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response

from accounts.permissions import IsApprovedPermissions
from listing.models import Property, PropertyType, PropertyAmenity, PropertyFeature, TestGis
from listing.serializers import PropertySerializer, PropertyTypeSerializer, PropertyAmenitySerializer, \
    PropertyFeatureSerializer, TestSerializer


# Create your views here.



class PropertyGenericView(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()
    permission_classes = [permissions.AllowAny]




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



class TestGenericView(generics.ListCreateAPIView):
    serializer_class = TestSerializer
    queryset = TestGis.objects.all()
    permission_classes = [permissions.AllowAny]



#property type - get, post, delete and put apis

class PropertyTypeGenericView(generics.ListCreateAPIView):
    queryset = PropertyType.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, permissions.DjangoModelPermissions]
    serializer_class = PropertyTypeSerializer

    lookup_field = 'id'




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



