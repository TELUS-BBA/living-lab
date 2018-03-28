from rest_framework import viewsets
from testresults.models import Iperf3Result, PingResult
from testresults.serializers import Iperf3ResultSerializer, PingResultSerializer


class Iperf3ResultViewSet(viewsets.ModelViewSet):
    queryset = Iperf3Result.objects.all()
    serializer_class = Iperf3ResultSerializer


class PingResultViewSet(viewsets.ModelViewSet):
    queryset = PingResult.objects.all()
    serializer_class = PingResultSerializer
