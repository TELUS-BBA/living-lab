# iperf3-mux
This repo contains a way of getting around iperf3's inability to conduct multiple simultaneous tests on a single iperf3 server.

It uses twisted to listen for a single utf-8 formatted message: "SENDPORT\r\n". When it receives this message it starts up an iperf server as a sub-process on a port between 10001 and 20000 inclusive, and sends that port back. If any errors occur, the server closes the connection. The server that is started as a sub-process is only good for one test; if one wants to do multiple tests one must get another server port by sending SENDPORT again.

To use, install twisted and iperf3 and then run it using ./server.py. If you want to change the port that the server listens on, I'm sure you can figure that out :)
