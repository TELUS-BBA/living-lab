from provisioning.models import NanoPi
from rest_framework import serializers


class NanoPiSerializer(serializers.ModelSerializer):
    ssh_port = serializers.SerializerMethodField()
    
    class Meta:
        model = NanoPi
        fields = ['id', 'ssh_port', 'username', 'password', 'apparent_ip',
                  'add_date', 'location_info', 'misc_info']

    def get_ssh_port(self, obj):
        return obj.id + 6000
