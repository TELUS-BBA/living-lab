from django.contrib import admin
from testresults.models import Iperf3Result, PingResult

admin.site.register(Iperf3Result)
admin.site.register(PingResult)
