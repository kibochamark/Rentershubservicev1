from tkinter.font import names

from django.urls import  path
from rest_framework.decorators import api_view
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import api_home, AccountDetail, AccountCreateView,DestroyAccountDetail, \
    AccountsViewSet

urlpatterns=[
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('create/user/', AccountCreateView.as_view(), ),
    path('update/user/<int:pk>', AccountsViewSet.as_view({
        'patch':'patch'
    }), ),
    path('users', AccountsViewSet.as_view({'get': 'list'})),
    path('test/<int:pk>/delete', DestroyAccountDetail.as_view())
]
