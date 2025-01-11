from django.contrib.gis.db import models

# Create your models here.
class Property(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.ForeignKey('PropertyType', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    # Location Details
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    location = models.PointField()

    # Features and Amenities
    features = models.ManyToManyField('PropertyFeature', blank=True)
    amenities = models.ManyToManyField('PropertyAmenity', blank=True)



    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    # ADDITIONAL DATA

    size = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    parking_spaces = models.IntegerField()

    # ... other fields ...
    is_available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    rent_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Image storage
    main_image_url = models.JSONField(blank=True, null=True)  # URL of the featured image
    images = models.JSONField(default=list)  # List of image objects (ID + URL)

    def __str__(self):
            return self.title





class PropertyFeature(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class PropertyType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



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
    parking_spaces = models.PositiveIntegerField(Null=True , Blank=True)
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)

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