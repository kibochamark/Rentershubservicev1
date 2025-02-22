import datetime
from http import HTTPStatus
from logging import raiseExceptions

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.db.models.expressions import result
from django.shortcuts import render, get_object_or_404
from django.views import View
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import  Response
from rest_framework import  generics, permissions
from rest_framework.views import APIView

from accounts.models import RentersUser, RentersRole, Otp
from accounts.serializers import AccountSerializer, RegisterSerializer, RoleSerializerModel, OtpSerializer
from rest_framework import  viewsets

from accounts.util import send_otp, generate_otp, get_tokens_for_user, verify_otp
from django.utils import timezone


from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings


from urllib.parse import urljoin

import requests
from django.urls import reverse
import os



# Create your views here.


# @api_view(["POST"])
# def api_home(request, *args, **kwargs):
#     postdata= request.data
#     serializer = AccountSerializer(data=postdata)
#     if serializer.is_valid(raise_exception=True):
#         print(serializer.data)
#         # serializer.save()
#         return Response(postdata)
#     return Response({
#         'error':'invalid data'
#     }, status=400)


#
# # generic api views
#
# class AccountDetail(generics.RetrieveAPIView):
#     queryset = RentersUser.objects.all()
#
#     serializer_class = AccountSerializer
#
#     # lookup_field ='pk'
#
#
#
#
#
# class DestroyAccountDetail(generics.DestroyAPIView):
#     queryset = RentersUser.objects.all()
#
#     serializer_class = AccountSerializer
#
#     # lookup_field ='pk'
#
#
# # class AccountCreateView(generics.CreateAPIView):
# #     queryset = RentersUser.objects.all()
# #
# #     serializer_class = RegisterSerializer
# #
# #
# #     # authentication_classes= [authentication.TokenAuthentication]
# #     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#





class AccountsViewSet(viewsets.ViewSet):
    queryset=RentersUser.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        elif self.action == "loginuser" or self.action == 'create' :
            print(self.action)
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]




    def loginuser(self, request):
        """login user and generate token"""

        try:
            contact = request.data.get("contact")
            password = request.data.get("password")

            obj =get_object_or_404(self.queryset, contact = contact)

            #print(obj.username)

            if not obj:
                return Response({
                    "error":"user does not exist"
                }, status=HTTPStatus.NOT_FOUND)

            if not password:
                return Response({
                    "error":"password is required"
                }, status=HTTPStatus.BAD_REQUEST)


            #print(obj.approval_status)

            if obj.approval_status != "APPROVED":
                return Response({
                    "error": "Please wait to be approved by admin"
                }, status=HTTPStatus.BAD_REQUEST)

            #print(obj.email, password)

            user = authenticate(request, username=obj.email, password=password)
            #print(user)

            if not user:
                return Response({
                    "error":"failed to authorize"
                }, status=HTTPStatus.NOT_FOUND)

            login(request, user)

            tokens =get_tokens_for_user(obj)


            #print(tokens)

            return Response({
                "result":{
                    "tokens":tokens,
                    "user_id":obj.id,
                    "role":obj.role.name
                }
            }, status=HTTPStatus.OK)


        except Exception as e:
            return Response({
                "error":"failed to get resource"
            }, status=HTTPStatus.BAD_REQUEST)




    @extend_schema(responses=AccountSerializer)
    def list(self, request):
        """
        Get all users
        """
        queryset = RentersUser.objects.all()

        data=AccountSerializer(queryset, many=True, context={'request': request}).data
        return Response({
            "message":"success",
            "result":data
        })

    @extend_schema(responses=RegisterSerializer)
    def create(self, request):
        """
        Create an instance of a user
        """
        body = request.data
        serializer = RegisterSerializer(data=body, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.CREATED)
        return  Response(RegisterSerializer.errors, status=HTTPStatus.BAD_REQUEST)


    @extend_schema(responses=AccountSerializer)
    def retrieve(self, request, pk=None):
        """
        retrieve an instance of a user
        """
        obj=get_object_or_404(self.queryset, pk=pk)
        result=None
        if obj:
            result=AccountSerializer(obj, context={'request': request}).data
            return Response({
                "message": "success",
                "result": result
            }, status=HTTPStatus.OK)
        return  Response({
            "message": "error",
            "result": f"obj with id {pk} does not exist"
        }, status=HTTPStatus.BAD_REQUEST)


    def update(self, request):
        pass

    @extend_schema(responses=RegisterSerializer)
    def patch(self, request, pk=None):
        """
                partially update an instance of a user
                """
        permission_classes=[permissions.IsAuthenticated]
        # print(request.data, pk)
        obj= get_object_or_404(self.queryset, pk=pk)
        serializer = RegisterSerializer(obj, data=request.data,
                                         partial=True, context={'request':request})  # set partial=True to update a data partially
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=200)
        return Response(data=serializer.errors, status=HTTPStatus.BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Delete an instance of a user
        """
        if pk is None:
            return Response(
                {"error": "Id is required"},
                status=HTTPStatus.BAD_REQUEST
            )

        # Retrieve the object to delete
        obj = get_object_or_404(self.queryset, pk=pk)

        # Perform the delete action
        obj.delete()

        return Response(
            {"message": f"Resource with ID {pk} has been successfully deleted"},
            status=HTTPStatus.OK
        )





class RolesViewSet(viewsets.ViewSet):
    """
    Renters Role apis-
    landlord, groundagent, admin
    """
    queryset=RentersRole.objects.all()
    serializer=RoleSerializerModel

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]




    @extend_schema(responses=RoleSerializerModel)
    def list(self, request):
        """
        Get all users
        """
        queryset = RentersRole.objects.all()

        data=self.serializer(queryset, many=True, context={'request': request}).data
        return Response({
            "message":"success",
            "result":data
        })




    @extend_schema(responses=RoleSerializerModel)
    def create(self, request):
        """
        Create an instance of a user
        """
        body = request.data
        serializer = self.serializer(data=body)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.CREATED)
        return  Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


    @extend_schema(responses=RoleSerializerModel)
    def retrieve(self, request, pk=None):
        """
        retrieve an instance of a user
        """
        obj=get_object_or_404(self.queryset, pk=pk)
        result=None
        if obj:
            result=self.serializer(obj, context={'request': request}).data
            return Response({
                "message": "success",
                "result": result
            }, status=HTTPStatus.OK)
        return  Response({
            "message": "error",
            "result": f"obj with id {pk} does not exist"
        }, status=HTTPStatus.BAD_REQUEST)


    def update(self, request):
        pass

    @extend_schema(responses=RoleSerializerModel)
    def patch(self, request, pk=None):
        """
                partially update an instance of a user
                """
        permission_classes=[permissions.IsAuthenticated]
        # print(request.data, pk)
        obj= get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer(obj, data=request.data,
                                         partial=True)  # set partial=True to update a data partially
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=200)
        return Response(data=serializer.errors, status=HTTPStatus.BAD_REQUEST)


    def destroy(self, request, pk=None):
        """
        Delete an instance of a user
        """
        if pk is None:
            return Response(
                {"error": "Id is required"},
                status=HTTPStatus.BAD_REQUEST
            )

        # Retrieve the object to delete
        obj = get_object_or_404(self.queryset, pk=pk)

        # Perform the delete action
        obj.delete()

        return Response(
            {"message": f"Resource with ID {pk} has been successfully deleted"},
            status=HTTPStatus.OK
        )




# class LoginView(APIView):
#     permission_classes = [permissions.AllowAny]
#
#         # test login  view
#      def post(self, request, *args, **kwargs):
#          phone = request.data.get('phone')
#          print(phone)
#          try:
#              user = User.objects.get(phone=phone)
#              print(user)
#              # Check for max OTP attempts
#              if int(user.max_otp_try) == 0 and user.otp_max_out and timezone.now() < user.otp_max_out:
#                  return Response(
#                  "Max OTP try reached, try after an hour",
#                  status=status.HTTP_400_BAD_REQUEST,
#                  )
#              # Generate OTP and update user record
#              otp = random.randint(1000, 9999)
#              otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
#              max_otp_try = int(user.max_otp_try) - 1
#              user.otp = otp
#              user.otp_expiry = otp_expiry
#              user.max_otp_try = max_otp_try
#              if max_otp_try == 0:
#                 otp_max_out = timezone.now() + datetime.timedelta(hours=1)
#              elif max_otp_try == -1:
#                 user.max_otp_try = 3
#              else:
#                  user.otp_max_out = None
#                  user.max_otp_try = max_otp_try
#                  user.save()
#                  print(user.otp, 'OTP', user.phone)
#                  send_otp(user.phone, otp, user)
#                  return Response("Successfully generated OTP", status=status.HTTP_200_OK)
#          except ObjectDoesNotExist:
#              user_ = User.objects.create(phone=phone)
#              print(user_)
#              otp = random.randint(1000, 9999)
#              otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
#              max_otp_try = int(user_.max_otp_try) - 1
#              user_.otp = otp
#              user_.otp_expiry = otp_expiry
#              user_.max_otp_try = max_otp_try
#              if max_otp_try == 0:
#                 otp_max_out = timezone.now() + datetime.timedelta(hours=1)
#              elif max_otp_try == -1:
#                 user_.max_otp_try = 3
#              else:
#                  user_.otp_max_out = None
#                  user_.max_otp_try = max_otp_try
#                  user_.is_passenger = True
#                  user_.save()
#                  send_otp(user_.phone, otp, user_)
#                  return Response("Successfully generated OTP", status=status.HTTP_200_OK)
#              # else:
#              # return Response("Phone number is incorrect", status=status.HTTP_401_UNAUTHORIZED)
#



# api to handle and generate otp

class OtpViewset(viewsets.ViewSet):


    queryset= RentersUser.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        print(self.action)
        if self.action == 'create' or self.action == 'verifyandupdatepassword' or self.action == "verifyotp":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


    # @extend_schema(responses=RegisterSerializer)
    def create(self, request):
        try:
            contact = request.data.get('contact')
            if not contact:
                return Response({
                    "error":"contact should be available"
                }, status=HTTPStatus.BAD_REQUEST)


            print(contact)


            otp=generate_otp()

            # # # add secret to otp
            # #
            #obj = Otp.objects.filter(secret=secret_key).first()
            # #
            # #
            # # print(obj, "non")


            # if obj is not None:
            #     serializer = OtpSerializer(obj, data={
            #         "secret":secret_key
            #     },  partial=True)
            #     if serializer.is_valid(raise_exception=True):
            #         serializer.save()
            # else:

            #     serializer = OtpSerializer(data={
            #         "secret": secret_key
            #     })
            #     print(serializer.is_valid())
            #     if serializer.is_valid(raise_exception=True):
            #         serializer.save()



            # print(otp, secret_key)
            send_otp(mobile=contact, otp=otp)


            return Response({
                "message": f"Otp sent successfully to {contact} , otp -{otp}"
            }, status=HTTPStatus.OK)

        except Exception as e:
            return Response({
                "error":"failed to create resource"
            }, status=HTTPStatus.BAD_REQUEST)



    @extend_schema(responses=RegisterSerializer)
    def verifyandupdatepassword(self, request):
        try:

            # print(request.user)

            contact = request.data.get('contact')
            password = request.data.get('password')
            user_otp= request.data.get('otp')


            # print(contact)

            if not contact and not user_otp or (not contact or not user_otp):
                return Response({
                    "error": "Missing required fields"
                }, status=HTTPStatus.BAD_REQUEST)

            obj = get_object_or_404(RentersUser, contact=contact)

            # print(obj.username)

            if not obj:
                return Response({
                    "error": "user not found"
                }, status=HTTPStatus.BAD_REQUEST)


            # print(obj.otp_secret)

            if not verify_otp(int(user_otp), secret_key=obj.otp_secret):
                return Response({
                    "error": "invalid otp"
                }, status=HTTPStatus.BAD_REQUEST)

            password = make_password(password)
            serializer = RegisterSerializer(obj, data={
                "password":password,
                "otp":user_otp,
                "max_out_otp":3
            }, partial=True, context={'request':request})


            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({
                    "message": "Password changed successfully"
                }, status=HTTPStatus.OK)

            return Response({
                "error": "something went wrong"
            }, status=HTTPStatus.BAD_REQUEST)

        except Exception as e:
            return Response({
                "error":"Failed to verify resource"
            }, status=HTTPStatus.BAD_REQUEST)



    def verifyotp(self, request):
        try:

            # print(request.user)

            user_otp = request.data.get('otp')

            # print(contact)

            if not user_otp :
                return Response({
                    "error": "Missing required fields"
                }, status=HTTPStatus.BAD_REQUEST)

          

            # print(obj.otp_secret)

            if not verify_otp(int(user_otp)):
                return Response({
                    "error": "invalid otp"
                }, status=HTTPStatus.BAD_REQUEST)



            return Response({
                "message": "Verified successfully"
            }, status=HTTPStatus.OK)

        except Exception as e:
            return Response({
                "error": "Failed to verify resource"
            }, status=HTTPStatus.BAD_REQUEST)



class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client


class GoogleLoginCallback(APIView):
    def get(self, request, *args, **kwargs):
        """
        If you are building a fullstack application (eq. with React app next to Django)
        you can place this endpoint in your frontend application to receive
        the JWT tokens there - and store them in the state
        """

        code = request.GET.get("code")

        if code is None:
            return Response(status=HTTPStatus.BAD_REQUEST)

        # Remember to replace the localhost:8000 with the actual domain name before deployment
        token_endpoint_url = urljoin("http://localhost:8000", reverse("google_login"))
        response = requests.post(url=token_endpoint_url, data={"code": code})

        return Response(response.json(), status=HTTPStatus.OK)





class LoginPage(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "pages/login.html",
            {
                "google_callback_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
                "google_client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            },
        )
