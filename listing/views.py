from http import HTTPStatus

import geocoder
from django.shortcuts import render
from rest_framework import generics, permissions

from listing.models import Property, PropertyType, PropertyAmenity
from listing.serializers import PropertySerializer, PropertyTypeSerializer, PropertyAmenitySerializer


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





class PropertyAmmenityGenericView(generics.ListCreateAPIView):
    queryset = PropertyAmenity.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, permissions.DjangoModelPermissions]
    serializer_class = PropertyAmenitySerializer


class UpdatePropertyAmenityGeneric(generics.RetrieveUpdateDestroyAPIView):
    queryset = PropertyAmenity.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, permissions.DjangoModelPermissions]
    serializer_class = PropertyAmenitySerializer

    lookup_field = 'id'



