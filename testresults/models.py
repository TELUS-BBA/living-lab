from django.db import models
from provisioning.models import NanoPi


class Iperf3Result(models.Model):
    nanopi = models.ForeignKey(NanoPi, on_delete=models.CASCADE)
    direction = models.CharField(max_length=4, choices=(('up', 'up'), ('down', 'down'),))
    bandwidth = models.DecimalField(max_digits=10, decimal_places=3)
    upload_date = models.DateTimeField(auto_now_add=True)


class PingResult(models.Model):
    nanopi = models.ForeignKey(NanoPi, on_delete=models.CASCADE)
    data = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    

class SockPerfResult(models.Model):
    pass
