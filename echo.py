#! /usr/bin/env python
# coding:utf-8

#Python2

#CONFIG==============
id=''
password=''
#====================

import base64
import datetime
import os
import urllib2

#get current global ip address
url = urllib2.urlopen('http://api.ghippos.net/ipcheck/')
currentIp = url.read()
url.close()

#check previous ip
previousIp = ''
previousEchoTime = ''
filePath = '/tmp/myip'

if not os.path.isfile(filePath):
	f = open(filePath, 'w')
	f.write(currentIp)
	f.close()
else:
	f = open(filePath, 'r')
	previousIp = f.read()
	f.close()

	fStamp = os.stat(filePath).st_mtime
	previousEchoTime = datetime.datetime.fromtimestamp(fStamp)

#echo
#1. different in current ip and previous ip
#2. 3 days have passed
if currentIp != previousIp or previousEchoTime + datetime.timedelta(days=3) < datetime.datetime.now():
	# basic auth is really fuck
	req = urllib2.Request('http://www.mydns.jp/login.html')
	authHeader = base64.encodestring('%s:%s' % (id, password))[:-1]
	req.add_header('Authorization', 'Basic ' + authHeader)
	url = urllib2.urlopen(req)
	url.read()

	print 'echo ip -> ' + currentIp

	f = open(filePath, 'w')
	f.write(currentIp)
	f.close()
#skip
else:
	print 'skip echo'
