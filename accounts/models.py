from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class RentersRole(models.Model):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        LANDLORD= "LANDLORD", 'Landlord'
        GROUNDAGENT = "GROUNDAGENT", 'GroundAgent'

    role = models.CharField(max_length=50, choices=Role.choices, unique=True)
    created_at= models.DateField(auto_created=True, auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    def __str__(self):
        return f"{self.role}"



# custom manager
class CustomUserManager(BaseUserManager):
    """
    Defines how the User(or the model to which attached)
    will create users and superusers.
    """
    def create_user(
        self,
        email,
        password,
        **extra_fields
        ):
        """
        Create and save a user with the given email, password,
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email) # lowercase the domain
        user = self.model(

            email=email,
            **extra_fields
        )

        user.set_password(password) # hash raw password and set
        user.save()
        return user
    def create_superuser(
        self,
        email,
        password,
        **extra_fields
        ):
        """
        Create and save a superuser with the given email,
        password, and date_of_birth. Extra fields are added
        to indicate that the user is staff, active, and indeed
        a superuser.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                "Superuser must have is_staff=True."
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must have is_superuser=True."
            )
        return self.create_user(
            email,
            password,
            **extra_fields
        )

class RentersUser(AbstractUser, models.Model):

    role= models.ForeignKey(RentersRole, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField("email address", unique=True)
    contact = models.CharField(max_length=11)
    created_at = models.DateField(auto_created=True, auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",

    ]  #


    objects = CustomUserManager()


    def __repr__(self):
        return f"{self.first_name} {self.last_name}"





