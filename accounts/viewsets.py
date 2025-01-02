from rest_framework import viewsets
from .models import RentersUser
from .serializers import AccountSerializer



class AccountViewSet(viewsets.ModelViewSet):
    queryset = RentersUser.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'pk'