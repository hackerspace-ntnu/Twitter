#!/usr/bin/env python

import subprocess
import time
import sys
from random import randint

try:
    import urllib2
except ImportError:
    import urllib.request as urllib2

from twitter import Twitter, OAuth, TwitterError
from secret import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_SECRET, CONSUMER_KEY

try:
    import pidentity

    PI_ID = getattr(pidentity, 'ID', '?')
except ImportError:
    PI_ID = '?'

TIMEOUT = 5


def is_internet_on():
    """Check if we have a connection to twitter.com"""
    try:
        urllib2.urlopen('http://twitter.com', timeout=1)
        return True
    except urllib2.URLError:
        pass
    return False


def get_serial():
    """Extract serial from cpuinfo file"""
    try:
        with open('/proc/cpuinfo', 'r') as open_file:
            for line in open_file:
                if line.startswith('Serial'):
                    return line[10:26]
    except:
        return "ERROR000000000"

    return "0000000000000000"


def get_ip():
    p = subprocess.Popen('ip route list', shell=True, stdout=subprocess.PIPE)
    data = p.communicate()
    split_data = data[0].split()
    return split_data[split_data.index('src') + 1]


try:
    while not is_internet_on():
        print("No internet connection detected, trying again in {}s".format(TIMEOUT))
        time.sleep(TIMEOUT)

    print("Internet connection detected!")
    while True:
        try:
            twitter = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
            print("Authed with twitter!")

            status = 'RPI-{id} <{rng}>({serial}) piip: {ip}'.format(
                id=PI_ID,
                rng=randint(1, 999),  # so that the new tweet is not identical to the last
                serial=get_serial(),
                ip=get_ip()
            )
            print(status)

            twitter.statuses.update(status=status)
            print("Tweeted!")
            break
        except TwitterError:
            print("TwitterError!! Trying again in {}s".format(TIMEOUT))
            time.sleep(TIMEOUT)
            continue

except KeyboardInterrupt:
    print("Stopping tweet-ip.py")
    sys.exit()
