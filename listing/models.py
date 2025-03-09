from django.contrib.gis.db import models

from accounts.models import RentersUser
from django.core.exceptions import  ValidationError
from django.core.validators import RegexValidator



def check_phone(value):
    if value:
        if len(value) != 10:
            raise ValidationError("Contact should be exactly 10 numbers with no countrycode")
        else:
            return value


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
    is_approved = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    rent_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Image storage
    main_image_url = models.JSONField(blank=True, null=True)  # URL of the featured image
    images = models.JSONField(default=list)  # List of image objects (ID + URL)

    posted_by=models.ForeignKey(RentersUser, on_delete=models.SET_NULL, null=True, blank=True)

    managed_by = models.CharField(max_length=255, null=True, blank=True, default="")
    owners_contact = models.CharField(max_length=255, null=True, blank=True, default="", validators=[check_phone])

    def __str__(self):
            return self.title




    class Meta:
        permissions = [
            ("can_verify_client", "Can verify client and ground agent authenticity"),
            ("can_record_leads", "Can record leads"),
            ("can_communicate_terms", "Can communicate terms and conditions"),
            ("can_guide_posting", "Can guide clients on posting properties"),
            ("can_approve_listings", "Can approve property listings"),
            ("can_edit_descriptions", "Can edit property descriptions"),
            ("can_share_client_info", "Can share client information with Admin P"),
            ("can_remind_posting", "Can remind clients to post properties"),
            ("can_request_property_info", "Can request property information from ground agents and digital marketers"),
            ("can_monitor_satisfaction", "Can monitor client satisfaction"),
            ("can_record_tenant_move_in", "Can record tenant move-in information"),
            ("can_invoice_clients", "Can invoice clients"),
            ("can_record_payments", "Can record payments"),
            ("can_ban_nonpaying_clients", "Can ban non-paying clients"),
        ]




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






class Connections(models.Model):
    connectionfullname=models.TextField(unique=True)
    contact = models.CharField(max_length=10, validators=[RegexValidator(
 regex=r"^\d{10}", message="Phone number must be 10 digits only.")], unique=True)
    

    propertylink = models.SlugField(max_length=2000, null=True)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True,blank=True)


    moved_in=models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    commission = models.DecimalField(max_digits=18, decimal_places=2)


    created_at = models.DateField(auto_created=True, auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    


    def __str__(self):
        return super().__str__(f"{self.connectionfullname} - {self.propertylink}")




class Revenue(models.Model):
    amount=models.DecimalField(max_digits=18, decimal_places=2)

    created_at = models.DateField(auto_created=True, auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    


    def __str__(self):
        return super().__str__(f"{self.amount} - {self.created_