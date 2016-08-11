#!/usr/bin/python
import urllib2
import json
import time

#Configuration
username='api'
password='yourpassword'
url="https://api.mailgun.net/v3/example.com/bounces?limit=10000"
output = 'output.csv'

# IMPORTANT: Must use time since epoch for time requests to Mailgun
# 86400 seconds per day * 30 days' retention = 2592000 seconds/month
date=str(int(time.mktime(time.gmtime()) - 2592000))


#HTTP Password manager setup
passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
#"None" starts manager for all transactions using url as base
passman.add_password(None,url,username,password)

#Create Authhandler, tell calls to urlopen to use it, and install it.
authhandler = urllib2.HTTPBasicAuthHandler(passman)
opener = urllib2.build_opener(authhandler)
urllib2.install_opener(opener)

#Start actually pulling data
print "Sending request to Mailgun."
data = (urllib2.urlopen(url)).read()

#De-JSONify the data we pulled
print "Parsing reply."
unencoded = json.loads(data)

buf = ''

#Iterate over the data and make it into CSV format
print "Formatting into CSV."
for x in range(0, len(unencoded["items"])):
  print "Processing " + str(x+1) + " of " + str(len(unencoded["items"])) + "."
  struct = unencoded["items"][x]
  buf += struct["address"]
  #Have to strip the newlines that some providers shove in their 5xx error messages so the fields come out legibly
  buf += ", " + struct["code"] + " " + struct["error"].replace('\n','') + "\r\n"


#Export the terrible horror we have created
print "Exporting."
dest = open(output, 'w')
dest.write(buf)
dest.close()
