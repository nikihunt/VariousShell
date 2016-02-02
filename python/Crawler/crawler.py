#!/usr/bin/python
#-*-encoding:utf-8-*-
import urllib2
import sys

def getPgae(url):
	response = urllib2.urlopen(url)
	return response.read()

def run(argvs):
	url = "http://www.cnblogs.com/loveyakamoz/archive/2011/07/21/2112832.html"
	page = getPgae(url)
	print page

if __name__ == "__main__":
	run(sys.argv)
