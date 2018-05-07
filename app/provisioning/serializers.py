from provisioning.models import NanoPi
from rest_framework import serializers
from datetime import datetime


class NanoPiSerializer(serializers.ModelSerializer):
    ssh_port = serializers.SerializerMethodField()
    
    class Meta:
        model = NanoPi
        fields = ('id', 'ssh_port', 'username', 'password', 'apparent_ip',
                  'add_date', 'location_info', 'misc_info')
        read_only_fields = ('id', 'ssh_port',)
        extra_kwargs = {'password': {'write_only': True}}

    def get_ssh_port(self, obj):
        return obj.id + 6000

    def create(self, validated_data):
        nanopi = NanoPi.objects.create(
            username=validated_data.get('username', None),
            apparent_ip=validated_data.get('apparent_ip', None),
            location_info=validated_data.get('location_info', ""),
            misc_info=validated_data.get('misc_info', ""),
            add_date=datetime.now()
        )
        nanopi.set_password(validated_data.get('password'))
        nanopi.save()
        return nanopi

    def update(self, instance, validated_data):
        instance.username=validated_data.get('username', instance.username)
        instance.apparent_ip=validated_data.get('apparent_ip', None)
        instance.location_info=validated_data.get('location_info', "")
        instance.misc_info=validated_data.get('misc_info', "")
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance
