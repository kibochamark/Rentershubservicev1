from http import HTTPStatus

from django.shortcuts import render, get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import  Response
from rest_framework import  generics, permissions

from accounts.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import authentication
from accounts.models import RentersUser
from accounts.serializers import AccountSerializer, RegisterSerializer
from rest_framework import  viewsets

# Create your views here.


@api_view(["POST"])
def api_home(request, *args, **kwargs):
    postdata= request.data
    serializer = AccountSerializer(data=postdata)
    if serializer.is_valid(raise_exception=True):
        print(serializer.data)
        # serializer.save()
        return Response(postdata)
    return Response({
        'error':'invalid data'
    }, status=400)



# generic api views

class AccountDetail(generics.RetrieveAPIView):
    queryset = RentersUser.objects.all()

    serializer_class = AccountSerializer

    # lookup_field ='pk'





class DestroyAccountDetail(generics.DestroyAPIView):
    queryset = RentersUser.objects.all()

    serializer_class = AccountSerializer

    # lookup_field ='pk'


class AccountCreateView(generics.CreateAPIView):
    queryset = RentersUser.objects.all()

    serializer_class = RegisterSerializer


    # authentication_classes= [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]







class AccountsViewSet(viewsets.ViewSet):
    queryset=RentersUser.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, DjangoModelPermissionsOrAnonReadOnly]

    @extend_schema(responses=AccountSerializer)
    def list(self, request):
        """
        Get all users
        """
        data=AccountSerializer(self.queryset, many=True, context={'request': request}).data
        return Response({
            "message":"success",
            "result":data
        })

    def create(self, request):
        pass

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
                                         partial=True)  # set partial=True to update a data partially
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=200)
        return Response(data=serializer.errors, status=HTTPStatus.BAD_REQUEST)

    def destroy(self, request):
        pass





