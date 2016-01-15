#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import urllib2
import json
import os
import setLogger
import logging
import sys
import time
import traceback
import re
import datetime

#set global var
ConsoleLog = setLogger.setLogger(logging.StreamHandler,logging.DEBUG)
FileLog = setLogger.setLogger(logging.FileHandler,logging.DEBUG)

host="http://10.103.16.49:9200"
indexPrefix="fast_news_all"
document="document"
queryjson="querystr.data"
idsize=50000000
targetfile="docid.data"
configfile="zl.properties"
startDate="2015-01-01 01:01:10"
endDate="2015-05-01 02:10:11"

sleeptime = 60

def logger(level,loginfo):
	global ConsoleLog
	global FileLog
	'''
	record logger info with console and file
	'''
	if loginfo is not None:
		if level == "debug":
			FileLog.debug(loginfo)
			ConsoleLog.debug(loginfo)
		elif level == "info":
			FileLog.info(loginfo)
			ConsoleLog.info(loginfo)
		elif level == "warn":
			FileLog.warn(loginfo)
			ConsoleLog.warn(loginfo)
		elif level == "error":
			FileLog.error(loginfo)
			ConsoleLog.error(loginfo)
		elif level == "critical":
			FileLog.critical(loginfo)
			ConsoleLog.critical(loginfo)

def loadConfig(conf,confDic):
	'''
	load config from identified file
	'''
	if os.path.exists(conf):
		if os.path.isfile(conf):
			with open(conf ,'r') as config:
				for line in config:
					lst = line.split("=")
					if(len(lst) == 2):
					    confDic[lst[0].strip(" ")] = (lst[1].strip(" ")).strip("\n")
					    logger("info","load config {0}".format(line))
					else:
						logger("error","bad config {0}".format(line))
			return True
		else:
			logger("error","config file {0} is not a file".format(conf))
			return False
	else:
		logger("error","config file {0} is not exist".format(conf))
		return False

def setParams(confDic):
	'''
	set global var by config
	'''
	global host,indexPrefix,document,queryjson,idsize,startDate,endDate,targetfile,configfile

	if confDic != None and len(confDic) != 0:
		#set configfile 
		if "configfile" in confDic.keys():
			configfile = confDic["configfile"]
		
		#load config from config file
		confFromFile = {}
		if configfile != '':
			if os.path.exists(configfile):
				 if not loadConfig(configfile,confFromFile):
				 	return False
			else:
				logger("error","cconfig file {0} is not exist".format(configfile))
				return False

		for key in confFromFile.keys():
			if key not in confDic.keys():
				confDic[key] = confFromFile[key]

		if "host" in confDic.keys() and confDic["host"] != '':
			host = confDic["host"]
			logger("info","set host:"+host)
		if "indexPrefix" in confDic.keys() and confDic["indexPrefix"] != '':
			indexPrefix = confDic["indexPrefix"]
			logger("info","set indexPrefix:"+indexPrefix)
		if "document" in confDic.keys() and confDic["document"] != '':
			document = confDic["document"]
			logger("info","set document:"+document)
		if "queryjson" in confDic.keys() and confDic["queryjson"] != '':
			queryjson = confDic["queryjson"]
			logger("info","set queryjson file:"+queryjson)
		if "idsize" in confDic.keys() and confDic["idsize"] != '':
			idsize = confDic["idsize"]
			logger("info","set idsize:"+idsize)
		if "startDate" in confDic.keys() and confDic["startDate"] != '':
			startDate = confDic["startDate"]
			logger("info","set startDate:"+startDate)
		if "endDate" in confDic.keys() and confDic["endDate"] != '':
			endDate = confDic["endDate"]
			logger("info","set endDate:"+endDate)
		if "targetfile" in confDic.keys():
			targetfile = confDic["targetfile"]
			logger("info","set targetfile:"+targetfile)
	return True

def generateRequest():
	'''
	generate url,request params data
	'''
	global host,indexPrefix,document,queryjson,idsize
	splitchar = '/'
        url = ''.join([host,splitchar,indexPrefix,splitchar,document,splitchar,"_search?size=",str(idsize)])
        f = file(queryjson)
        data = json.load(f)
        data["query"]["filtered"]["filter"]["range"]["date"]["gte"] = startDate
        data["query"]["filtered"]["filter"]["range"]["date"]["lte"] = endDate
        data = json.dumps(data)
        return url,data

def getResponse(req,data):
	'''
	fetch result from remote server with parameters identified in request
	'''
	page = urllib2.urlopen(req,data)
	data = page.read()
	return data

def parseResult(data):
	'''
	parse result whitch get from remote server 
	the result is json struct
	'''
	ids = []
	if data is not None:
		dic = json.loads(data)
		if dic is not None and "hits" in dic.keys():
		    orginalDic = dic["hits"]
		    if orginalDic is not None and "hits" in orginalDic.keys():
		    	targetList = orginalDic["hits"]
		    	if targetList is not None and len(targetList) != 0:
		    		for targetDic in targetList:
		    			if "_id" in targetDic.keys():
			    			docid = targetDic["_id"]
			    			if docid is not None and docid != '':
			    				ids.append(docid)
			logger("info","get {0} docids".format(len(ids)))
		else:
			logger("error","json load null data")
	else:
		logger("error","result is null")
	return ids

def write2File(data,filename):
	if data is not None and len(data) != 0:
		if filename is not None and filename != "":
			with open(filename,'w') as f:
				for id in data:
					f.write(id)
					f.write("\n")
		else:
			logger("error","write to file error,the filename {0} is null")
	else:
		logger("warn","write null data to file")

def write2FileC(data,filehandler):
	if data is not None and len(data) != 0:
		for id in data:
			filehandler.write(id)
			filehandler.write("\n")
	else:
		logger("warn","write null data to file")

def splitDate():
	'''
	split Date to months
	'''
	global startDate,endDate
	datelst = []
	if(startDate != "" and endDate != ""):
		sdlsttmp = startDate.split(" ")
		sdlst = sdlsttmp[0].split("-")
		sdlst.extend(sdlsttmp[1].split(":"))
		edlsttmp = endDate.split(" ")
		edlst = edlsttmp[0].split("-")
		edlst.extend(edlsttmp[1].split(":"))
		syear = sdlst[0];smonth = sdlst[1];sday = sdlst[2];shour = sdlst[3];smin = sdlst[4];ssec  =sdlst[5]
		eyear = edlst[0];emonth = edlst[1];eday = edlst[2];ehour = edlst[3];emin = edlst[4];esec  =edlst[5]
		if syear == eyear and smonth == emonth:
			datelst.append([startDate,endDate])
		else:
			year = int(syear);day = sday;hour = shour;minu = smin;sec = ssec
			splitflag1 = "-";splitflag2 = ":"
			start = startDate
			end = startDate
			for i in range(int(smonth)+1,(int(eyear)-int(syear))*12+int(emonth)):
				year = year + i/12
				end = ''.join([str(year),splitflag1,str(i),splitflag1,day," ",hour,splitflag2,minu,splitflag2,sec])
				datelst.append([start,end])
				start = end
			datelst.append([start,endDate])
	return datelst

def RequestwithSplitDate():
	'''
	'''
	global sleeptime
	url,data = generateRequest()
	datelst = splitDate()
	try:
		filehandler = open(targetfile,'a')
		if datelst != None and len(datelst) != 0:
			f = file(queryjson)
			dictdata = json.load(f)
			for i in range(len(datelst)):
				datepair = datelst[i]
				dictdata["query"]["filtered"]["filter"]["range"]["date"]["gte"] = datepair[0]
				dictdata["query"]["filtered"]["filter"]["range"]["date"]["lte"] = datepair[1]
				reqdata = json.dumps(dictdata)
				result = getResponse(url,reqdata)
				ids = parseResult(result)
				write2FileC(ids,filehandler)
				logger("info","{0}s month [{1} -- {2}] doc ids has record".format(i+1,datepair[0],datepair[1]))
				if i < len(datelst)-1:
					time.sleep(sleeptime)
	except Exception, e:
		logger("error",traceback.format_exc())
	finally:
		filehandler.close()
	
def checkDate(datetime):
	prog = re.compile("^(19|20)\d\d-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01]) [0-2][0-3]:[0-5][0-9]:[0-5][0-9]$")
	if prog.match(datetime)!=None:
		return True
	else:
		logger("error","date {0} is invalid date format, valid date format :YYYY-mm-dd HH:MM:SS".format(datetime))
		return False

def checkbeforeExcute():
	'''
	check something before excute
	'''
	global queryjson,targetfile,startDate,endDate

	#check query json file is exist or not
	if not os.path.exists(queryjson):
		logger("error","queryjson file {0} is not exist".format(queryjson))
		return False
	
	#check the Date format's validity
	if not checkDate(startDate) or not checkDate(endDate):
		return False

	#check startDate is after endDate or not
	starttime = time.mktime(datetime.datetime.strptime(startDate, "%Y-%m-%d %H:%M:%S").timetuple())
	endtime = time.mktime(datetime.datetime.strptime(endDate, "%Y-%m-%d %H:%M:%S").timetuple())
	if starttime >= endtime:
		logger("error","startDate {0} is after endDate {1}".format(startDate,endDate))
		return False

	#check targetfile is exist(will overwrite) or not
	while os.path.exists(targetfile):
		print "warn","the file you will storing the result is exist :{0} \n".format(targetfile)
		flag = raw_input("would you like to change a file ?")
		if flag.lower() == "n" or flag.lower == "no":
			break;
		else:
			targetfile = raw_input("please input a new filename:")
	return True

def run(argv):
	confDic = {}

	#read configfile and key-val pairs
	if len(argv) > 1:
		argv = argv[1:]
		for pair in argv:
			tmp = pair.split("=")
			if(len(tmp)==2 and tmp[0]!="" and tmp[1]!=""):
				confDic[str.strip(tmp[0])] = str.strip(tmp[1])
			else:
				logger("error","bad parameters :{0}".format(pair))
				return

	#set params,command line params will overwrite file params
	setParams(confDic)

	#check before excute
	if not checkbeforeExcute():
		return
	
	#generate request
	requrl,reqdata = generateRequest()

	#get response
	data = getResponse(requrl,reqdata)

	#parse response
	ids = parseResult(data)

	#record ids in file
	write2File(ids,targetfile)

def runWithSplitDate(argv):
	confDic = {}

	#read configfile and key-val pairs
	if len(argv) > 1:
		argv = argv[1:]
		for pair in argv:
			tmp = pair.split("=")
			if(len(tmp)==2 and tmp[0]!="" and tmp[1]!=""):
				confDic[str.strip(tmp[0])] = str.strip(tmp[1])
			else:
				logger("error","bad parameters :{0}".format(pair))
				return

	#set params,command line params will overwrite file params
	if not setParams(confDic):
		return

	#check before excute
	if not checkbeforeExcute():
		return
	#request with sllit date
	RequestwithSplitDate()

def test():
	'''
	test
	'''
	global startDate,endDate
	checkDate(startDate)
	datelst = splitDate()
	for datepair in datelst:
		print datepair[0],datepair[1],"\n"


if __name__ == "__main__":
	'''
	you should excute the python file with the following format
	python findDocid.py key1=val1 key2=val2 key3=val3 ...... 
	'''
	#run(sys.argv)
	#test()
	runWithSplitDate(sys.argv)



