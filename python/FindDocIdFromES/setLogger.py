#-*- coding: utf-8 -*-

import os
import sys
import logging
import time

#获取当前时间
def getCurrentTime(TimeFormat="%Y-%m-%d-%X"):
	return time.strftime(TimeFormat,time.localtime())

#设置log,sys.path[0]为当前脚本所在目录
def setLogger(Handler=logging.StreamHandler,LogLevel=logging.NOTSET,loggername="",LogDestination=sys.path[0]):
        if loggername == "":
		loggername = str(time.time())
		time.sleep(0.01)
	logger = logging.getLogger(loggername)
	logHandler = logging.StreamHandler()
	if Handler == logging.StreamHandler:
		logHandler = Handler()
	elif Handler == logging.FileHandler:
		dirpath = LogDestination+os.sep+getCurrentTime("%Y-%m-%d")
		if not os.path.exists(dirpath):
			os.makedirs(dirpath)
		LogDestination = dirpath+os.sep+getCurrentTime("%H")+".log"#不能用getCurrentTime("%X")，因为%X格式（h:m:s）中带有":"符号，而文件名中不能出现该符号		
		logHandler = Handler(LogDestination)

	logger.addHandler(logHandler)
	formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
	logHandler.setFormatter(formatter)
	logger.setLevel(LogLevel)
	return logger

if __name__ == '__main__':
	logger = setLogger(logging.StreamHandler)
	logger.debug("logger is ready")
	logger.debug("Log's parameters are : Handler, Destination, Level")
