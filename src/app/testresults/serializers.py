from testresults.models import Iperf3Result, PingResult, SockPerfResult
from rest_framework import serializers


class Iperf3ResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Iperf3Result
        fields = ['id', 'nanopi', 'direction', 'bandwidth', 'upload_date']


class PingResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PingResult
        fields = ['id', 'nanopi', 'state', 'time', 'upload_date']


class SockPerfResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SockPerfResult
        fields = ['id', 'nanopi', 'latency', 'upload_date']
