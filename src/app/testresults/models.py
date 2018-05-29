from django.db import models
from provisioning.models import NanoPi


class Iperf3Result(models.Model):
    nanopi = models.ForeignKey(NanoPi, on_delete=models.CASCADE)
    direction = models.CharField(max_length=20, choices=(('up', 'up'), ('down', 'down'),))
    bandwidth = models.FloatField()
    upload_date = models.DateTimeField(auto_now_add=True)


class PingResult(models.Model):
    nanopi = models.ForeignKey(NanoPi, on_delete=models.CASCADE)
    state = models.CharField(max_length=4, choices=(('up', 'up'), ('down', 'down'),))
    time = models.DateTimeField() # the time of the ping
    upload_date = models.DateTimeField(auto_now_add=True) # the time that the group of pings was uploaded
    

class SockPerfResult(models.Model):
    nanopi = models.ForeignKey(NanoPi, on_delete=models.CASCADE)
    latency = models.FloatField()
    upload_date = models.DateTimeField(auto_now_add=True)
