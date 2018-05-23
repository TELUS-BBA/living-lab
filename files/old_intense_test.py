#!/usr/bin/env python3

import re

def run_iperf_test(host, port, test_func):
    with socket.create_connection((host, port), 2) as s:
        s.sendall("SENDPORT\r\n".encode())
        received_port = int(s.recv(4096).decode())
        time.sleep(1)
        result = test_func(host, received_port)
    return result


def test_up(iperf_host, iperf_port):
    regex = re.compile('^\[SUM\].*\s([0-9]+) Mbits/sec.*sender.*$')
    cmd = ['iperf3', '-c', iperf_host, '-p', str(iperf_port), '-P', '4']
    process = Popen(cmd, stdin=None, stdout=PIPE, stderr=STDOUT, bufsize=1)
    for line in iter(process.stdout):
        match = regex.search(line.decode())
        if match is not None:
            result = int(match.group(1))
    return result


def test_down(iperf_host, iperf_port):
    regex = re.compile('^\[SUM\].*\s([0-9]+) Mbits/sec.*sender.*$')
    cmd = ['iperf3', '-c', iperf_host, '-p', str(iperf_port), '-P', '4', '-R']
    process = Popen(cmd, stdin=None, stdout=PIPE, stderr=STDOUT, bufsize=1)
    for line in iter(process.stdout):
        print(line)
        match = regex.search(line.decode())
        if match is not None:
            result = int(match.group(1))
    return result


def intense_test2(host, port):
    print("testing up")
    print(run_iperf_test(host, port, test_up))
    print("testing down")
    print(run_iperf_test(host, port, test_down))
