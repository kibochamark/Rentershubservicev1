from django.contrib.gis.db import models

from accounts.models import RentersUser


# Create your models here.
class Property(models.Model):
    title = models.CharField(max_length=255, default="")
    description = models.TextField(default="")
    property_type = models.ForeignKey('PropertyType', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    # Location Details

    city = models.CharField(max_length=100, default="")
    state = models.CharField(max_length=100, default="")
    country = models.CharField(max_length=100, default="")
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    location = models.PointField(null=True, blank=True)
    address = models.CharField(max_length=255, default="")

    # Features and Amenities
    features = models.ManyToManyField('PropertyFeature', blank=True)
    amenities = models.ManyToManyField('PropertyAmenity', blank=True)



    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


    # ADDITIONAL DATA

    size = models.IntegerField(default=0)
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    parking_spaces = models.IntegerField(default=0)
    water_charges = models.DecimalField(decimal_places=2 , max_digits=12, default=0.00)
    garbage_charges = models.DecimalField(decimal_places=2 , max_digits=12, default=0.00)
    security_charges = models.DecimalField(decimal_places=2 , max_digits=12, default=0.00)
    other_charges = models.DecimalField(decimal_places=2 , max_digits=12, default=0.00)
    water_deposit = models.DecimalField(decimal_places=2 , max_digits=12, default=0.00)

    # ... other fields ...
    is_available = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    rent_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Image storage
    main_image_url = models.JSONField(blank=True, null=True)  # URL of the featured image
    images = models.JSONField(default=list)  # List of image objects (ID + URL)

    posted_by=models.ForeignKey(RentersUser, on_delete=models.SET_NULL, null=True, blank=True)
    managed_by = models.CharField(max_length=255, null=True, blank=True, default="")


    def __str__(self):
            return self.title







class PropertyType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class PropertyFeature(models.Model):
    propertytype=models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.TextField(unique=True)

    def __str__(self):
        return f" {self.propertytype}-{self.name}"



class PropertyAmenity(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name




class SpaceType(models.Model):
    property = models.ForeignKey(Property, related_name='space_types', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)  # e.g., '2-Bedroom', 'Studio'
    size_in_sqm = models.DecimalField(max_digits=6, decimal_places=2)
    num_bedrooms = models.PositiveIntegerField()
    num_bathrooms = models.PositiveIntegerField()
    parking_spaces = models.PositiveIntegerField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name} - {self.property.title}"



class Unit(models.Model):
    space_type = models.ForeignKey(SpaceType, related_name='units', on_delete=models.CASCADE)
    unit_number = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=[('vacant', 'Vacant'), ('occupied', 'Occupied'), ('reserved', 'Reserved')])

    def __str__(self):
        return f"Unit {self.unit_number} - {self.space_type.name}"




class UnitImage(models.Model):
    unit = models.ForeignKey(Unit, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField()
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.unit}"




class TestGis(models.Model):
    location= models.PointField()
    address=models.CharField(max_length=255, default="")


    def __str__(self):
        return self.location





