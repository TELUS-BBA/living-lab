#!/usr/bin/env python3

import subprocess
import re

output = subprocess.run(['netstat', '-tulpn'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode()

regex = re.compile(r'127\.0\.0\.1\:(6[0-9]{3,3})')
numbers = regex.findall(output)
numbers = list(map(lambda x: int(x), numbers))
numbers.sort()
print("Counted {} nanopis connected".format(len(numbers)))

template = "nanopi{id_number}:\n  ansible_port: {port_number}"
output_list = []
for number in numbers:
    output_list.append(template.format(id_number=number-6000, port_number=number))

yml_output = '\n'.join(output_list)
print(yml_output)
