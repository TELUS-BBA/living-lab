from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


class NanoPi(User):
    apparent_ip = models.GenericIPAddressField(blank=True, null=True, protocol='IPv4')
    add_date = models.DateTimeField(auto_now_add=True)
    location_info = models.TextField(blank=True)
    misc_info = models.TextField(blank=True)


@receiver(post_save, sender=NanoPi)
def add_to_nanopi_group(sender, instance, created, **kwargs):
    if created:
        try:
            g = Group.objects.get(name='nanopis')
        except ObjectDoesNotExist:
            g = Group(name='nanopis')
            g.save()
            iperf3permission = Permission.objects.get(name='Can add iperf3 result')
            pingpermission = Permission.objects.get(name='Can add ping result')
            sockperfpermission = Permission.objects.get(name='Can add sock perf result')
            g.permissions.add(iperf3permission, pingpermission, sockperfpermission)
        g.user_set.add(instance)
