from django.urls import  path
from rest_framework.decorators import api_view



from .views import AccountsViewSet, RolesViewSet, OtpViewset

urlpatterns=[
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('create/user/', AccountsViewSet.as_view({
        'post':'create'
    })),
    path('login/user/', AccountsViewSet.as_view({
        'post':'loginuser'
    })),
    path('update/user/<int:pk>', AccountsViewSet.as_view({
        'patch':'patch'
    }), ),
    path('users', AccountsViewSet.as_view({'get': 'list'})),
    path('user/<int:pk>/delete', AccountsViewSet.as_view({
        'delete':'destroy'
    })),
    path('user/<int:pk>/', AccountsViewSet.as_view({
        'get':'retrieve'
    })),


#     roles
    path('create/role/', RolesViewSet.as_view({
            'post':'create'
        })),
    path('update/role/<int:pk>', RolesViewSet.as_view({
        'patch':'patch'
    }), ),
    path('roles', RolesViewSet.as_view({'get': 'list'})),
    path('role/<int:pk>/delete', RolesViewSet.as_view({
        'delete':'destroy'
    })),
    path('role/<int:pk>/', RolesViewSet.as_view({
        'get':'retrieve'
    })),


#     urls
    path('create/otp', OtpViewset.as_view({
        'post':'create'
    }))

]
