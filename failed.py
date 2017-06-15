#!/usr/bin/python
import urllib2
import json
import time

#Configuration
username='api access username'
password='api access key'
domain = 'example.com'

#Setup access URL string.
#86400 seconds per day * 30 days' retention = 2592000
date=str(int(time.mktime(time.gmtime()) - 2592000))
url="https://api.mailgun.net/v3/"+domain+"/events?event=failed&ascending=yess&limit=100&begin="+date

#HTTP Password manager setup.
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

unencoded = json.loads(data)
buf = ''

# Parse entries and classify based on error.
for x in range(0, len(unencoded["items"])-1):
  struct = unencoded["items"][x]
  buf += struct["message"]["headers"]["to"]
  if struct["delivery-status"]["message"] != None:
    buf += ", " + struct["delivery-status"]["message"]
  if struct["delivery-status"]["description"] != None:
    buf += ", " + struct["delivery-status"]["description"] + "\r\n"
  else: buf += "\r\n"


#Export results to file.
dest = open("output", 'w')
dest.write(buf)
dest.close()
