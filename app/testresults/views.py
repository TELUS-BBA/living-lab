from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions
from testresults.models import Iperf3Result, PingResult
from testresults.serializers import Iperf3ResultSerializer, PingResultSerializer


class Iperf3ResultViewSet(ModelViewSet):
    queryset = Iperf3Result.objects.all()
    serializer_class = Iperf3ResultSerializer
    permission_classes = (DjangoModelPermissions,)


class PingResultViewSet(ModelViewSet):
    queryset = PingResult.objects.all()
    serializer_class = PingResultSerializer
    permission_classes = (DjangoModelPermissions,)
