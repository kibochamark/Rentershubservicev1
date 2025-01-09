from rest_framework import serializers

from listing.models import Property


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields=[
            'name',
            'location',
            'address']
        read_only_fields=['location']