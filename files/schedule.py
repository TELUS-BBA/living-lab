#!/usr/bin/env python3

from apscheduler.schedulers.blocking import BlockingScheduler
import maya
import iperf3
import socket
import time
import requests
from requests.auth import HTTPBasicAuth
import json
from subprocess import check_call, DEVNULL, STDOUT, CalledProcessError
import threading
import argparse
from copy import copy


def get_nanopi_info(path):
    with open(path, 'r') as fd:
        return json.loads(fd.read())


def check_lock_nonblocking(func):
    """Decorator for functions that require lock to be free. If the lock is not free it
       does not execute func."""
    def wrapper(*args, **kwargs):
        if network_lock.acquire(blocking=False):
            try:
                func(*args, **kwargs)
                network_lock.release()
            except:
                network_lock.release()
                raise
    return wrapper


def check_lock_blocking(func):
    """Decorator for functions that require lock to be free. Blocks until the lock is free."""
    def wrapper(*args, **kwargs):
        network_lock.acquire(blocking=True)
        try:
            func(*args, **kwargs)
            network_lock.release()
        except:
            network_lock.release()
            raise
    return wrapper


# ---------------------------------------------------------------------
# Intense Test
# ---------------------------------------------------------------------


def do_iperf_test(host, port, iperf_test):
    """Gets a port from the iperf3 mux server and runs the iperf3 test given in iperf_test"""
    with socket.create_connection((host, port), 2) as s:
        s.sendall("SENDPORT\r\n".encode())
        iperf_port = int(s.recv(4096).decode())
        iperf_test.port = iperf_port
        time.sleep(1)
        result = iperf_test.run()
    return result


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
        

@check_lock_blocking
def intense_test(info, iperf_host, iperf_port, post_url):
    print("Running intense test at {}".format(maya.now().rfc2822()))
    up_result = test_up(iperf_host, iperf_port)
    down_result = test_down(iperf_host, iperf_port)
    up_data = {
        'nanopi': info.get('id'),
        'direction': 'up',
        'bandwidth': up_result,
    }
    response = requests.post(post_url, json=up_data, auth=HTTPBasicAuth(info.get('username'), info.get('password')))
    down_data = {
        'nanopi': info.get('id'),
        'direction': 'down',
        'bandwidth': down_result,
    }
    response = requests.post(post_url, json=down_data, auth=HTTPBasicAuth(info.get('username'), info.get('password')))


# ---------------------------------------------------------------------
# Continuous/Gentle Test
# ---------------------------------------------------------------------
    

@check_lock_nonblocking
def continuous_test(info, host, results):
    print("Running continuous test at {}".format(maya.now().rfc2822()))
    cmd = ["ping", "-c", "1", "-W", "1", host]
    try:
        check_call(cmd, timeout=2, stdin=None, stdout=DEVNULL, stderr=STDOUT)
    except CalledProcessError:
        state = 'down'
    else:
        state = 'up'
    results.append({
        'nanopi': info.get('id'),
        'time': maya.now().rfc3339(),
        'state': state,
    })


# ---------------------------------------------------------------------
# Continuous/Gentle Test Upload
# ---------------------------------------------------------------------
    

@check_lock_blocking
def continuous_test_upload(info, host, port, location, results):
    print("Running continuous test upload at {}".format(maya.now().rfc2822()))
    list_to_upload = copy(results)
    results.clear()
    upload_url = "http://{}:{}{}".format(host, port, location)
    response = requests.post(upload_url, json=list_to_upload, auth=HTTPBasicAuth(info.get('username'), info.get('password')))
    return response


# ---------------------------------------------------------------------
# Schedule
# ---------------------------------------------------------------------


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('test_host')
    parser.add_argument('iperf_port')
    parser.add_argument('management_host')
    parser.add_argument('management_port')
    parser.add_argument('info_path')
    parser.add_argument('ping_result_path')
    parser.add_argument('intense_result_path')
    parser.add_argument('intense_test_minute')
    args = parser.parse_args()

    network_lock = threading.Lock()
    continuous_test_results = []
    info = get_nanopi_info(args.info_path)
    full_intense_result_path = "http://{}:{}{}".format(args.management_host, args.management_port, args.intense_result_path)
    full_ping_path = "http://{}:{}{}".format(args.management_host, args.management_port, args.ping_result_path)

    scheduler = BlockingScheduler()
#    scheduler.add_job(intense_test, args=(info, args.test_host, args.iperf_port, full_intense_result_path),
#                      trigger='cron', hour='*/1', minute=args.intense_test_minute)
    scheduler.add_job(continuous_test, args=(info, args.test_host, continuous_test_results), coalesce=True,
                      trigger='cron', second='*/2')
    scheduler.add_job(continuous_test_upload,
                      args=(info, args.management_host, args.management_port, args.ping_result_path,
                            continuous_test_results),
                      coalesce=True,
                      trigger='cron', minute='*/5')
    print("Starting scheduler...")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
