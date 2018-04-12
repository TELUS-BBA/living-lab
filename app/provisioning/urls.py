from rest_framework import routers
from provisioning.views import NanoPiViewSet


router = routers.DefaultRouter()
router.register(r'nanopi', NanoPiViewSet)
urlpatterns = router.urls
