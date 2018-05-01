#!/usr/bin/env python3

import argparse
from xkcdpass import xkcd_password as xp
from getpass import getpass
import requests
from requests.auth import HTTPBasicAuth
import json

API_HOST = "http://192.168.1.101:8000/provisioning/nanopi/"

parser = argparse.ArgumentParser()
parser.add_argument("user")
parser.add_argument("password")
parser.add_argument("hostname")
parser.add_argument("port")
args = parser.parse_args()

API_HOST = "http://{}:{}/provisioning/nanopi/".format(args.hostname, args.port)

# get MAC and parse into a string without colons (to be used as username)
mac = open('/sys/class/net/'+'eth0'+'/address').readline()
username = mac.replace(":", "")

# generate random password that can still be typed by a human
wordfile = xp.locate_wordfile()
mywords = xp.generate_wordlist(wordfile=wordfile, min_length=4, max_length=6)
password =  xp.generate_xkcdpassword(mywords, numwords=4).replace(" ", "")

# get admin credentials from whoever is calling this
#admin_username = input("API Admin Username: ")
#admin_password = getpass(prompt="API Admin Password: ")

# post the username and password to API
response = requests.post(API_HOST, data={'username': username, 'password': password},
                         auth=HTTPBasicAuth(args.user, args.password))
response.raise_for_status()
print("Success: provisioned NanoPi with username {} and password {}".format(username, password))

# write results to file
with open('/home/nanopi/info') as fd:
    info = {"username": username, "password": password, "port": port}
    fd.write(json.dumps(info))
