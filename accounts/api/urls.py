from rest_framework.routers import DefaultRouter
from .views import AccountViewSet

router = DefaultRouter()
router.register(r"", AccountViewSet, basename="account")

app_name = "api"
urlpatterns = router.urls
