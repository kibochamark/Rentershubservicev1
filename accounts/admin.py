from django.contrib import admin

from accounts.models import RentersUser, RentersRole, Otp

# Register your models here.
admin.site.register(RentersUser)
admin.site.register(RentersRole)
admin.site.register(Otp)
