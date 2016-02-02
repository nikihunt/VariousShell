#-*-coding:utf8-*-
import sys
import os

if __name__=="__main__":
    filename = sys.argv[1]
    count = int(sys.argv[2])
    value=""
    storefile="es_filter.data"
    if os.path.exists(filename):
        with open(filename,'r') as f:
            value = f.readline()
        with open(storefile,'a') as f:
            for i in range(0,count):
                f.write(value)