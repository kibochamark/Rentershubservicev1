from accounts.models import RentersUser, RentersRole
from django.contrib.auth.models import User
from rest_framework import  serializers


class RoleSerializer(serializers.Serializer):
    role=serializers.CharField(read_only=True)


class AccountSerializer(serializers.ModelSerializer):
    role_name = RoleSerializer(source='role', read_only=True)
    # url= serializers.HyperlinkedIdentityField(view_name='account-detail', lookup_field='pk')
    class Meta:
        model=RentersUser
        fields=[
            'pk',
            'first_name',
            'email',
            'contact',
            'role_name',
            'username'
        ]





class RegisterSerializer(serializers.ModelSerializer):


    class Meta:
        model=RentersUser
        fields=[
            'email',
            'password',
            'first_name',
            'last_name',
            'role',
            'contact',
            'username'
        ]




class RoleSerializerModel(serializers.ModelSerializer):
    class Meta:
        model=RentersRole
        fields=[
            'pk',
            'role'
        ]