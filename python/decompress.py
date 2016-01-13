#-*- coding: utf-8 -*-
import os
import sys
import gzip
import logging
import time
import setLogger




#package全局变量
logger = setLogger.setLogger(logging.StreamHandler)	

#获取当前脚本所在目录
def getCurrentDir():
	return sys.path[0]
	
def read_gz_file(path,fileHandle):
    if os.path.exists(path):
        with gzip.open(path, 'rb') as pf:
            for line in pf:
            	fileHandle.write(line)
    else:
        logger.error('the path [{}] is not exist!'.format(path))

def read_file_list(path):
	if os.path.exists(path):
		FileNameList = []
		for filename in os.listdir(path):
			FileNameList.append(filename)
		return FileNameList
	else:
		logger.error('the path [{}] is not exist!'.format(path))

def isFormatFile(FileName,fileFormat):
	splitparts = []
	splitparts = FileName.split('.')
	length = len(splitparts)
	if length > 0 and splitparts[length-1] == fileFormat:
		return True
	else:
		return False

def getFun(fileFormat):
	if fileFormat.strip() != '' and fileFormat.strip() != None:
		if fileFormat == 'gz':
			logger.debug("support .gz format")
			return read_gz_file
	else:
		return None

def isContainFormatFile(path,fileFormat):
	FileNameList = []
	FileNameList = read_file_list(path)
	if len(FileNameList) == 0:
		return False
	else:
		for FileName in FileNameList:
			if isFormatFile(FileName,fileFormat):
				return True
		return False




def decompress(CompressDirPath,fileFormat,decompresspath):
	if CompressDirPath.strip() == '' or CompressDirPath == None:
		logger.error('parameter CompressDirPath is null')
	elif fileFormat.strip() == '' or fileFormat == None:
		logger.error('parameter fileFormat is null')
	elif decompresspath.strip() == '' or decompresspath == None:
		logger.error('parameter decompresspath is null')
	else:
		if os.path.exists(CompressDirPath):
			if isContainFormatFile(CompressDirPath,fileFormat):
				FileNameList = []
				FileNameList = read_file_list(CompressDirPath)
				fun = getFun(fileFormat)
				if fun != None:
					if len(FileNameList) > 0:
						with open(decompresspath,'w') as mergeFile:
							for FileName in FileNameList:
								if isFormatFile(FileName,fileFormat):
									filepath = CompressDirPath+'\\'+FileName
									logger.debug("decompress file : {0}".format(filepath))
									fun(filepath,mergeFile)
					else:
						logger.error('system cannot get the FileName List of paht .{0}!'.format(CompressDirPath))
				else:
					logger.error('system not support the .{0} file!'.format(fileFormat))
			else:
				logger.error('the compress Dir path {0} is not contain .{1} file!'.format(CompressDirPath,fileFormat))
		else:
			logger.error('the compress Dir path [{}] is not exist!'.format(CompressDirPath))

def test():
	testDirpath = getCurrentDir()+os.sep+'CompressDir'
	testFilepath = testDirpath+os.sep+'test.txt'
	fileFormat = 'gz'
	decompresspath = testDirpath+os.sep+'decompress.txt'
	decompress(testDirpath,fileFormat,decompresspath)
	FileContent = []
	DecompressFileContent = []
	with open(testFilepath,'r') as originalfile:
		for line in originalfile:
			FileContent.append(line)
	with open(decompresspath,'r') as decompressfile:
		for line in decompressfile:
			DecompressFileContent.append(line)
	if FileContent != '' and DecompressFileContent != '':
		if ''.join(FileContent) == ''.join(DecompressFileContent):
			print 'decompress module is ready!'



#命令行输入格式：python 脚本名称 压缩文件所在目录 压缩文件格式 解压路径
if __name__ == "__main__":
	test()
