from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
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

    def create(self, request, *args, **kwargs):
        is_list = isinstance(request.data, list)
        if not is_list:
            return super(PingResultViewSet, self).create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
