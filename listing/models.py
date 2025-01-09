from django.contrib.gis.db import models

# Create your models here.


class Property(models.Model):
    name= models.CharField(max_length=20)
    location=models.PointField()
    address=models.CharField(max_length=200)




    def __str__(self):
        return self.name