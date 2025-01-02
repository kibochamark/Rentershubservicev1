#     serializer validation
from rest_framework import serializers
from .models import RentersUser
def validate_first_name(self, value):
            qs=RentersUser.objects.filter(first_name__iexact = value)
            if qs.exists():
                raise serializers.ValidationError(f"{value} already existe")
            return value


# from rest_framework import UniqueValidator