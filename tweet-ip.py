#!/usr/bin/env python3

from twitter import *
import subprocess
from random import randint
import time

from urllib.request import urlopen, URLError
from secret import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_SECRET, CONSUMER_KEY


def internet_on():
    try:
        response=urlopen('http://twitter.com',timeout=1)
        return True
    except URLError as err: pass
    return False

def getserial():
    # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
      f = open('/proc/cpuinfo','r')
    for line in f:
        if line[0:6]=='Serial':
            cpuserial = line[10:26]
    f.close()
  except:
      cpuserial = "ERROR000000000"

  return(cpuserial)

while not internet_on():
    print("no internetz")
    time.sleep(5)

print("internetz!")
rng = randint(1, 999)

complete = None

while not complete:
    try:
        time.sleep(2)
        twitter = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))
        print("Authed with twitter!")
        arg='ip route list'
        p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
        data = p.communicate()
        split_data = data[0].split()
        ipaddr = split_data[split_data.index(b'src')+1].decode("utf-8")

        my_ip = 'RPI-*num* <%d>(%s) piip: %s' %  (rng,getserial(), ipaddr)
        print(my_ip)

        twitter.statuses.update(status=my_ip)
        print("tweeted!")
        complete = True
    except TwitterError:
        print("TwitterError!! Trying again")
        continue
