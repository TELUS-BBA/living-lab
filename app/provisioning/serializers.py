from provisioning.models import NanoPi
from rest_framework import serializers


class NanoPiSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NanoPi
        fields = ['id', 'username', 'password', 'apparent_ip', 'add_date', 'location_info', 'misc_info']
