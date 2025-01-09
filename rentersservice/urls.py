"""
URL configuration for rentersservice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import  get_schema_view
from rest_framework.documentation import include_docs_urls
from drf_spectacular.views import  SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/listing/', include('listing.urls')),
        path('api-auth/', include('rest_framework.urls')),
    # path('docs/', include_docs_urls(title='RentersHubAPi')),
    # path('schema', get_schema_view(
    #     title="Renters Hub Service",
    #     description="Real estate apis",
    #     version="1.0.0"
    # ), name="openapi-schema"),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    path('', SpectacularSwaggerView.as_view(url_name='schema')),
path('api/login/', include('rest_social_auth.urls_jwt_pair')),


]
