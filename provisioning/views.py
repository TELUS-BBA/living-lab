from rest_framework import viewsets
from provisioning.models import NanoPi
from provisioning.serializers import NanoPiSerializer


class NanoPiViewSet(viewsets.ModelViewSet):
    queryset = NanoPi.objects.all()
    serializer_class = NanoPiSerializer
