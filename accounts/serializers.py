import datetime

from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from django.contrib.auth.hashers import make_password


from accounts.models import RentersUser, RentersRole, Otp
from django.contrib.auth.models import User
from rest_framework import  serializers


class RoleSerializer(serializers.Serializer):
    role=serializers.CharField(read_only=True)


class AccountSerializer(serializers.ModelSerializer):
    role_name = RoleSerializer(source='role', read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    terms_and_conditions = serializers.SerializerMethodField(read_only=True)
    # url= serializers.HyperlinkedIdentityField(view_name='account-detail', lookup_field='pk')
    class Meta:
        model=RentersUser
        fields=[
            'pk',
            'first_name',
            'last_name',
            'email',
            'contact',
            'role_name',
            'username',
            'status',
            'terms_and_conditions',

        ]

    def get_status(self, obj):
        return  obj.approval_status


    def get_terms_and_conditions(self, obj):
        return "accepted" if obj.isAcceptedTermsAndConditions else "rejected"




class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentersUser
        fields = [
            'email',
            'password',
            'first_name',
            'last_name',
            'role',
            'contact',
            'username'
        ]
        extra_kwargs = {
            'password': {'write_only': True}  # Ensures the password is write-only
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # Hash the password
        return super().create(validated_data)







class RoleSerializerModel(serializers.ModelSerializer):
    class Meta:
        model=RentersRole
        fields=[
            'pk',
            'role'
        ]



class OtpSerializer(serializers.ModelSerializer):
        class Meta:
            model=Otp
            fields=[
                'secret'
            ]
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentersUser
        fields = [
            'email',
            'password',
            'first_name',
            'last_name',
            'role',
            'contact',
            'username',
            'status'
        ]
        extra_kwargs = {
            'password': {'write_only': True}  # Ensures the password is write-only
        }

    def update(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # Hash the password
        return super().create(validated_data)

