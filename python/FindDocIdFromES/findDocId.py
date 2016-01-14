#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import os


def loadConfig(conf):
	'''
	load config from identified file
	'''
	confDic = {}
	if os.path.exists(conf) and os.path.isfile(conf):
		with open(conf ,'r') as config:
			for line in config:
				lst = config.split(":")
				if(len(lst) == 2):




def fetchResult(url):
	'''
	fetch result from remote server with parameters identified in url
	'''
	page = urllib.urlopen(url)
	data = page.read()
	return data


def parseResult(data):
	'''
	parse result whitch get from remote server 
	the result is json struct
	'''
	data = file(data)
	dic = json.load(data)
	ids = []
	if dic is not None:
	    orginalDic = dic["hits"]
	    if orginalDic is not None:
	    	targetList = orginalDic["hits"]
	    	if targetList is not None and len(targetList) != 0:
	    		for targetDic in targetList:
	    			docid = targetDic["_id"]
	    			if docid is not None and docid != '':
	    				ids.append(docid)
	print len(ids)
	return ids

def write2File(data,filename):
	if data is not None and len(data) != 0:
		with open(filename,'w') as f:
			for id in data:
				f.write(id)
				f.write("\n")
if __name__ == "__main__":
	filename = "docid.data"
	data = "13.data"
	if len(argv) == 2:
		filename = argv[1]
	if len(argv) == 3:
		filename = argv[2]
		data = argv[1]
	lst = parseResult(data)
	write2File(lst,filename)
