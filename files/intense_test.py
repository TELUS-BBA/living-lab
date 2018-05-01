#!/usr/bin/env python3

import iperf3
import socket
import time


HOST = "192.168.1.101"
PORT = 10000


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
        print("sending SENDPORT")
        s.sendall("SENDPORT\r\n".encode())
        iperf_port = int(s.recv(4096).decode())
        print("running test")
        iperf_test.port = iperf_port
        time.sleep(1)
        result = iperf_test.run()
    return result


if __name__ == "__main__":

    # do tests
    up_result = test_up(HOST, PORT)
    print("up result: {}".format(up_result))
    down_result = test_down(HOST, PORT)
    print("down result: {}".format(down_result))
    jitter_result = test_jitter(HOST, PORT)
    print("jitter result: {}".format(jitter_result))

    # send data to API (to be completed)
