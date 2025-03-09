from http import HTTPStatus

import django_filters.rest_framework
import geocoder
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry
from django.shortcuts import render, get_object_or_404
from geocoder import location
from rest_framework import generics, permissions, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.contrib.gis.measure import D

from accounts.models import RentersUser
from accounts.permissions import IsApprovedPermissions, CanEditDescriptions, CanApproveListings
from accounts.util import get_geocode, send_message
from listing.filterset import PropertyFilter
from listing.models import Property, PropertyType, PropertyAmenity, PropertyFeature, Revenue, TestGis, SpaceType, Unit
from listing.serializers import PropertySerializer, PropertyTypeSerializer, PropertyAmenitySerializer, \
    PropertyFeatureSerializer, RevenueSerializer, SpaceTypeSerializer, UnitSerializer


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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PropertyTypeSerializer

    lookup_field = 'id'

   


    def get_queryset(self, *args, **kwargs):
        qs = self.queryset.order_by('id')
        print(qs)

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

    #filterset_fields=('title')
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsApprovedPermissions]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsApprovedPermissions]
    #filter_backends = []
    filterset_class =PropertyFilter


    def get_queryset(self, *args, **kwargs):
        userid = self.request.query_params.get("userid", None)

        #get lang and long variables
        address = self.request.query_params.get("address", None)


    
        qs = super().get_queryset().filter()

        if address:
            status, data= get_geocode(address)

            # print(generated_location, status, data)
    
            if status == 200:
                pnt= GEOSGeometry('POINT(' + str(data['lon']) + ' ' + str(data['lat']) + ')', srid=4326)
                # matching_query=qs.annotate(distance=Distance('location', pnt)).order_by('distance')
                matching_query = qs.annotate(distance=Distance("location", pnt)).filter(distance__lte=D(km=5)) | qs.filter(address__icontains=address)
                qs = matching_query

        if userid:
            newqs = qs.filter(posted_by=int(userid)).all().order_by('title', "-id")
            return newqs
        return qs


    def perform_create(self, serializer):
        address = serializer.initial_data["address"]
        features = serializer.initial_data["features"]
        amenities = serializer.initial_data["amenities"]
        posted_by = serializer.initial_data["posted_by"]



        # print(address, features, amenities, posted_by)

        #get geocode from address

        generated_location=None
        status, data= get_geocode(address)

        print(generated_location, status, data)

        if status == 200:
            pnt= GEOSGeometry('POINT(' + str(data['lon']) + ' ' + str(data['lat']) + ')')
            generated_location = pnt


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


        if serializer.is_valid(raise_exception=True):
            message="""
A new property that needs your immediate attention has been uploaded on Renters Hub.

"""
            send_message('0740399167', message)
            return serializer.save(location=generated_location, features=feature_set, amenities=amenities_set, posted_by=self.request.user)

        return Response({
            "error":"Something went wrong"
        }, status=500)



class UpdatePropertyGeneric(generics.RetrieveUpdateDestroyAPIView):
    """update and delete property"""
    queryset = Property.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsApprovedPermissions, CanEditDescriptions, CanApproveListings]
    serializer_class = PropertySerializer
    filterset_class =PropertyFilter

    lookup_field = 'id'

    def perform_update(self, serializer):
        status = serializer.initial_data.get("is_approved", None)
        address = serializer.initial_data.get("address", None)

        generated_location = None
        
        if serializer.is_valid(raise_exception=True):



            if status and status == True:
                
                obj = get_object_or_404(self.queryset, id=int(self.kwargs.get('id')))
                if obj:

                    message=f"""
                    CONGRATULATIONS! The property you listed on Renters Hub has been approved. See how it appears on the website https://rentershub.co.ke/property/{obj.id}”
                    """
            
                    send_message(obj.owners_contact, message)



            if address:
                resstatus, data = get_geocode(address)
                if resstatus == 200:
                    pnt = GEOSGeometry('POINT(' + str(data['lon']) + ' ' + str(data['lat']) + ')')
                    return  serializer.save(location=pnt)
            return serializer.save()




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




# revenue
class RevenueGeneric(generics.ListCreateAPIView):
    queryset = Revenue.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsApprovedPermissions]
    serializer_class = RevenueSerializer

    

class RevenueUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Revenue.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsApprovedPermissions, permissions.IsAdminUser, CanApproveListings, CanEditDescriptions]
    serializer_class = RevenueSerializer

    lookup_field='id'




# summary

class SummaryViewSet(viewsets.ViewSet):
    permissions_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        print(self.action)
        if self.action == 'get_admin_summary' or self.action == "get_tenant_groundagent_summary":
            permission_classes = [permissions.IsAuthenticated, IsApprovedPermissions]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


    def get_tenant_groundagent_summary(self, request, user_id=None):

        """
        retrieve total no of properties
        retrieve total no of approved properties
        retrieve total no of pending properties

        per user
        
        """

        user = get_object_or_404(RentersUser, id=user_id)

        if user is None:
            return Response({
                "error":"User does not exist"
            }, status=404)
        
        listings=Property.objects.filter(posted_by=user_id).exists()


        if listings is None:

            return Response({
                "error":"User does not have existing properties"
            }, status=200)
        

        approved_count = Property.objects.filter(is_approved=True).count()
        pending_count = Property.objects.filter(is_approved=False).count()
        total_count=Property.objects.count()


        return Response({
            "approved_properties":approved_count,
            "pending_properties":pending_count,
            "total_properties":total_count

        }, status=200)
    

    def get_admin_summary(self, request):
        user= request.user

    
        if user.role is None:
            return Response({
                "error":"You dont have an existing role"
            }, status=403)

        if  user.role.role != "ADMIN":
            return Response({
                "error":"you are not authorized to perform this action"
            }, status=403)
        

        approved_count = Property.objects.filter(is_approved=True).count()
        pending_count = Property.objects.filter(is_approved=False).count()
        total_count=Property.objects.count()
        approved_landlords_count=RentersUser.objects.filter(role__role="LANDLORD", is_approved=False).count()
        pending_landlords_count=RentersUser.objects.filter(role__role="LANDLORD", is_approved=True).count()
        pending_groundagents_count=RentersUser.objects.filter(role__role="GROUNDAGENT", is_approved=False).count()
        pending_admins_count=RentersUser.objects.filter(role__role="ADMIN", is_approved=False).count()
        approved_admins_count=RentersUser.objects.filter(role__role="ADMIN", is_approved=True).count()
        approved_groundagents_count=RentersUser.objects.filter(role__role="GROUNDAGENT", is_approved=True).count()
        total_count=Property.objects.count()
        total_admins=RentersUser.objects.filter(role__role="ADMIN").count()
        total_landlords=RentersUser.objects.filter(role__role="LANDLORD").count()
        total_groundagents=RentersUser.objects.filter(role__role="GROUNDAGENT").count()
        total_users=RentersUser.objects.count()


        return Response({
            "approved_properties":approved_count,
            "pending_properties":pending_count,
            "total_properties":total_count,


            "total_users":total_users,
            "totaladmins":total_admins,
            "total_landlords":total_landlords,
            "total_groundagents":total_groundagents,

            "approved_admins":approved_admins_count,
            "pending_admins":pending_admins_count,

            "approved_landlords":approved_landlords_count,
            "pending_landlords":pending_landlords_count,

            "approved_agents":approved_groundagents_count,
            "pending_agents":pending_groundagents_count

        }, status=200)
        



        



