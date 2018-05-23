from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from django.db.models.signals import post_save
from django.dispatch import receiver
from provisioning.models import NanoPi
from provisioning.serializers import NanoPiSerializer


class NanoPiViewSet(viewsets.ModelViewSet):
    queryset = NanoPi.objects.all()
    serializer_class = NanoPiSerializer
    permission_classes = (DjangoModelPermissions,)
