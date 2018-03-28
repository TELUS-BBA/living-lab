from django.db import models


class NanoPi(models.Model):
    mac_address = models.CharField(max_length=50)
    apparent_ip = models.GenericIPAddressField(protocol='IPv4')
    add_date = models.DateTimeField(auto_now_add=True)
