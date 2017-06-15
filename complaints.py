#!/usr/bin/python
import urllib2
import json
import time

#Configuration
username='api access username'
password='yourpassword'
url="https://api.mailgun.net/v3/example.com/complaints?limit=10000"
output = 'output.csv'

# IMPORTANT: Have to use time since epoch for Mailgun pulls
# 86400 seconds per day * 30 days' retention = 2592000 secs/month
date=str(int(time.mktime(time.gmtime()) - 2592000))

#HTTP Password manager setup
passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
#None starts manager for all transactions using url as base
passman.add_password(None,url,username,password)

#Create Authhandler, tell calls to urlopen to use it.
authhandler = urllib2.HTTPBasicAuthHandler(passman)
opener = urllib2.build_opener(authhandler)
urllib2.install_opener(opener)

#Start actually pulling data
response = urllib2.urlopen(url)
data=response.read()

#De-JSONify the data we pulled
unencoded = json.loads(data)

#Iterate over the data and make it into CSV format
buf = {}
for x in range(0, len(unencoded["items"])):
  struct = unencoded["items"][x]
  buf[struct["address"]] = struct["created_at"]


#Now deal with sorting based on date
from datetime import datetime

#New list with just the dates pulled from our unsorted data
a = []
for x in buf.keys():
  a.append(''.join(map(str,buf[x])))

#Sort list based on date
a.sort(key = lambda date: datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z"))


#Horrible unoptimized multiple loop that goes over the entire data set for every. single. date.

iter = 0
count = 0
finalbuf = ''

#Iterate (badly) over everything and sort them out
while iter < len(buf):
  for key,val in buf.iteritems():
    if val == a[count]:
      used = key
      finalbuf += val + ", " + key + "\r\n"
#Need to remove used keys from our data so they won't be iterated over again
  buf.pop(key)
  count += 1


#Export the terrible horror we have created
dest = open(output, 'w')
dest.write(finalbuf)
dest.close()
