from rest_framework import routers
from testresults.views import Iperf3ResultViewSet, PingResultViewSet


router = routers.DefaultRouter()
router.register(r'iperf3', Iperf3ResultViewSet)
router.register(r'ping', Iperf3ResultViewSet)
urlpatterns = router.urls
