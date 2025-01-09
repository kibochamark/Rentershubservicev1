from http import HTTPStatus

import geocoder
from django.shortcuts import render
from rest_framework import generics, permissions

from listing.models import Property
from listing.serializers import PropertySerializer


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
            print(geo.json)
            lat=geo.latlng[0]
            lng=geo.latlng[1]
            point=f"Point({str(lng)} {str(lat)}"

        return serializer.save(location=point)


            