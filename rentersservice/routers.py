from rest_framework.routers import DefaultRouter

from accounts.viewsets import AccountViewSet

router=DefaultRouter()
router.register('accounts-abc', AccountViewSet, basename='accounts')



urlpatterns=router.urls