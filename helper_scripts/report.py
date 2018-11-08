#!/usr/bin/env python3

# Summarizes nginx access.log by counting the number of each HTTP
# status code that happened in the current day.
# Needs a bit of work to make it more general.

import os
import re
from datetime import datetime
import requests
from collections import Counter

os.chdir('management/logs/')
report = []

with open('access.log', 'rt') as fd:
    access = fd.read()

re_string = r'(.*{}.*'.format(datetime.now().strftime('%d/%b/%Y')) + ' ([1-5][0-9]{2}) [0-9]+.*)'
date_re = re.compile(re_string)
matches = date_re.findall(access)
report.append('Found {} entries for today'.format(len(matches)))
strings, statuses = zip(*matches)
count_of_statuses = Counter(statuses)
report.append("Status\tCount")
for element in count_of_statuses:
    report.append('{status}\t{count}'.format(status=element, count=count_of_statuses.get(element)))

with open('reports/{}.txt'.format(datetime.now().date()), 'wt') as fd:
    print(*report, sep='\n', end='\n', file=fd)
