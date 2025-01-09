from django.urls import path

from listing.views import PropertyGenericView

urlpatterns=[
    path('properties', PropertyGenericView.as_view(), name="properties")
]