from django.contrib import admin
from testresults.models import Iperf3Result, PingResult, SockPerfResult

admin.site.register(Iperf3Result)
admin.site.register(PingResult)
admin.site.register(SockPerfResult)
