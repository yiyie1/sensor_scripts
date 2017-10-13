#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import os.path
import fnmatch
import xlrd
import xlwt
import sys
#rootdir = os.getcwd()

logfiles = []
length = []

#for parent, dirnames, filenames in os.walk(rootdir): #遍历路径获取父目录，子文件夹名（不含路径）和文件名
#	for filename in filenames:
#		print "parent is:" + parent
#		print "filename is:" +filename
#		print "the full name of the file is:" + os.path.join(parent,filename)
		

def getSNR(f):
	snr = 0
	for line in f:
		if "snr" in line:
			snrr = line.split("nr:")[1].strip()
			snr = snrr.split()[0]
			break
	return snr


def run(rootdir):
	for dir, subdir, filenames in os.walk(rootdir):
		for filename in filenames:
			if fnmatch.fnmatch(filename, "*_log.txt"):
				logfile = os.path.join(dir, filename)
				logfiles.append(logfile)

	filename = xlwt.Workbook()
	sheet = filename.add_sheet("my_sheet")
	row = 0
	for file in logfiles:
		col = 0
		sheet.write(row,col,file)
		col = 1
		with open(file) as f:
			sheet.write(row,col,getSNR(f))
		row = row + 1

	filename.save("SNR.xls")

	print ("{} files processed...".format(len(logfiles)))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		run(sys.argv[1])
	else:
		print("python SNR_extract.py <directory>")
	


				
