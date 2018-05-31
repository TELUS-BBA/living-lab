#!/usr/bin/env python3

import argparse
from xkcdpass import xkcd_password as xp
from getpass import getpass
import requests
from requests.auth import HTTPBasicAuth
import json
import random

parser = argparse.ArgumentParser()
parser.add_argument("user")
parser.add_argument("password")
parser.add_argument("hostname")
parser.add_argument("port")
parser.add_argument("nanopi_provisioning_path")
parser.add_argument("info_path")
args = parser.parse_args()

API_HOST = "http://{}:{}{}".format(args.hostname, args.port, args.nanopi_provisioning_path)

# get MAC and parse into a string without colons (to be used as username)
mac = open('/sys/class/net/'+'eth0'+'/address').readline()
username = mac.replace(":", "").rstrip()

# generate random password that can still be typed by a human
wordfile = xp.locate_wordfile()
mywords = xp.generate_wordlist(wordfile=wordfile, min_length=4, max_length=6)
password =  xp.generate_xkcdpassword(mywords, numwords=4).replace(" ", "")

# get admin credentials from whoever is calling this
#admin_username = input("API Admin Username: ")
#admin_password = getpass(prompt="API Admin Password: ")

# update/create the API record of the nanopi
get_response_json = requests.get(API_HOST, auth=HTTPBasicAuth(args.user, args.password)).json()
same_username = [nanopi for nanopi in get_response_json if (nanopi.get('username') == username)]
if len(same_username) > 0:
    response = requests.put(API_HOST+'{}/'.format(same_username[0].get('id')),
                            data={'username': username, 'password': password},
                            auth=HTTPBasicAuth(args.user, args.password))
else:
    response = requests.post(API_HOST, data={'username': username, 'password': password},
                             auth=HTTPBasicAuth(args.user, args.password))
response.raise_for_status()
response_json = response.json()

# write results to file
with open(args.info_path, 'w+') as fd:
    response_json['username'] = username
    response_json['password'] = password
    fd.write(json.dumps(response_json))

print(response_json.get('ssh_port'))
