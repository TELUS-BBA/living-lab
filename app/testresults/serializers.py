from testresults.models import Iperf3Result, PingResult
from rest_framework import serializers


class Iperf3ResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Iperf3Result
        fields = ['id', 'nanopi', 'direction', 'bandwidth', 'upload_date']


class PingResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PingResult
        fields = ['id', 'nanopi', 'data', 'upload_date']
