#!/usr/bin/env python3
from apscheduler.schedulers.blocking import BlockingScheduler
import maya
import iperf3
import socket
import time
import requests
from requests.auth import HTTPBasicAuth
import json


IPERF_HOST = {{ iperf_host }}
IPERF_PORT = {{ iperf_port }}
MANAGEMENT_HOST = "localhost"
MANAGEMENT_PORT = 5000
POST_URL = "http://{}:{}/testresults/iperf3/".format(MANAGEMENT_HOST, MANAGEMENT_PORT)


def get_nanopi_info():
    with open('/home/nanopi/info', 'r') as fd:
        return json.loads(fd.read())


# ---------------------------------------------------------------------
# Intense Test
# ---------------------------------------------------------------------


def test_up(host, port):
    test_client = iperf3.Client()
    test_client.server_hostname = host
    test_client.num_streams = 4
    result = do_iperf_test(host, port, test_client)
    return result.sent_Mbps


def test_down(host, port):
    test_client = iperf3.Client()
    test_client.server_hostname = host
    test_client.num_streams = 4
    test_client.reverse = True
    result = do_iperf_test(host, port, test_client)
    return result.sent_Mbps


def test_jitter(host, port):
    test_client = iperf3.Client()
    test_client.server_hostname = host
    test_client.num_streams = 4
    test_client.protocol = 'udp'
    result = do_iperf_test(host, port, test_client)
    return result.jitter_ms
        

def do_iperf_test(host, port, iperf_test):
    """Gets a port from the iperf3 mux server and runs the iperf3 test given in iperf_test"""
    with socket.create_connection((host, port), 2) as s:
        s.sendall("SENDPORT\r\n".encode())
        iperf_port = int(s.recv(4096).decode())
        print("running test")
        iperf_test.port = iperf_port
        time.sleep(1)
        result = iperf_test.run()
    return result


def intense_test():
    print("Running intense test at {}".format(maya.now().rfc2822()))
    up_result = test_up(IPERF_HOST, IPERF_PORT)
    print("up result: {}".format(up_result))
    down_result = test_down(IPERF_HOST, IPERF_PORT)
    print("down result: {}".format(down_result))
    info = get_nanopi_info()
    up_data = {
        'nanopi': info.get('id'),
        'direction': 'up',
        'bandwidth': up_result,
    }
    response = requests.post(POST_URL, up_data, auth=HTTPBasicAuth(info.get('username'), info.get('password')))
    down_data = {
        'nanopi': info.get('id'),
        'direction': 'up',
        'bandwidth': down_result,
    }
    response = requests.post(POST_URL, down_data, auth=HTTPBasicAuth(info.get('username'), info.get('password')))


# ---------------------------------------------------------------------
# Continuous Test Upload
# ---------------------------------------------------------------------
    

def continuous_test():
    print("Running continuous test at {}".format(maya.now().rfc2822()))


# ---------------------------------------------------------------------
# Schedule
# ---------------------------------------------------------------------


if __name__ == "__main__":
    info = get_nanopi_info()
    scheduler = BlockingScheduler()
    scheduler.add_job(intense_test, 'cron', hour='*/1', minute=info.get('test_time'))
    scheduler.add_job(continuous_test, 'cron', minute='*/5')
    print("Starting scheduler...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
