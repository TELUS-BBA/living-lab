from provisioning.models import NanoPi
from rest_framework import serializers


class NanoPiSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NanoPi
        fields = ['id', 'mac_address', 'apparent_ip', 'add_date']
