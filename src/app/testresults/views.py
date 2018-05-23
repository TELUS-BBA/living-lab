from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
from django_filters import rest_framework as filters
from testresults.models import Iperf3Result, PingResult, SockPerfResult
from testresults.serializers import Iperf3ResultSerializer, PingResultSerializer, SockPerfResultSerializer


class TestResultPagination(CursorPagination):
    page_size = 100
    ordering = 'id'


class Iperf3ResultFilter(filters.FilterSet):
    class Meta:
        model = Iperf3Result
        fields = {
            'id': ['exact'],
            'nanopi': ['exact'],
            'direction': ['exact'],
            'bandwidth': ['exact', 'lt', 'gt'],
            'upload_date': ['exact', 'month', 'month__gt', 'month__lt', 'day', 'day__gt', 'day__lt',
                            'hour', 'hour__gt', 'hour__lt'],
        }


class PingResultFilter(filters.FilterSet):
    class Meta:
        model = PingResult
        fields = {
            'id': ['exact'],
            'nanopi': ['exact'],
            'state': ['exact'],
            'time': ['exact', 'month', 'month__gt', 'month__lt', 'day', 'day__gt', 'day__lt',
                     'hour', 'hour__gt', 'hour__lt'],
            'upload_date': ['exact', 'month', 'month__gt', 'month__lt', 'day', 'day__gt', 'day__lt',
                            'hour', 'hour__gt', 'hour__lt'],
        }


class SockPerfResultFilter(filters.FilterSet):
    class Meta:
        model = SockPerfResult
        fields = {
            'id': ['exact'],
            'nanopi': ['exact'],
            'latency': ['exact', 'lt', 'gt'],
            'upload_date': ['exact', 'month', 'month__gt', 'month__lt', 'day', 'day__gt', 'day__lt',
                            'hour', 'hour__gt', 'hour__lt'],
        }


class Iperf3ResultViewSet(ModelViewSet):
    queryset = Iperf3Result.objects.all()
    serializer_class = Iperf3ResultSerializer
    permission_classes = (DjangoModelPermissions,)
    pagination_class = TestResultPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = Iperf3ResultFilter


class PingResultViewSet(ModelViewSet):
    queryset = PingResult.objects.all()
    serializer_class = PingResultSerializer
    permission_classes = (DjangoModelPermissions,)
    pagination_class = TestResultPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PingResultFilter

    def create(self, request, *args, **kwargs):
        is_list = isinstance(request.data, list)
        if not is_list:
            return super(PingResultViewSet, self).create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class SockPerfResultViewSet(ModelViewSet):
    queryset = SockPerfResult.objects.all()
    serializer_class = SockPerfResultSerializer
    permission_classes = (DjangoModelPermissions,)
    pagination_class = TestResultPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SockPerfResultFilter
