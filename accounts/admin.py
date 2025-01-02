from django.contrib import admin

from accounts.models import RentersUser, RentersRole

# Register your models here.
admin.site.register(RentersUser)
admin.site.register(RentersRole)