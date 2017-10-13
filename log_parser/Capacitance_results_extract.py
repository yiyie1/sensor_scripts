#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import os.path
import fnmatch
import xlrd
import xlwt
import linecache
import sys
#rootdir = os.getcwd()

logfiles = []
length = []

#for parent, dirnames, filenames in os.walk(rootdir): #遍历路径获取父目录，子文件夹名（不含路径）和文件名
#	for filename in filenames:
#		print "parent is:" + parent
#		print "filename is:" +filename
#		print "the full name of the file is:" + os.path.join(parent,filename)

def getSS(f):
	ss = 0
	for line in f:
		if "Signal Strength Median: " in line:
			ss = line.split("Signal Strength Median: ")[1].strip()
	return ss
	
def getUnif(f):
	Unif = 0
	for line in f:
		if "Uniformity" in line:
			Unifor = line.split("Uniformity: ")[1].strip()
			Unif = Unifor.split("(")[0].strip()
	return Unif
	
def getBlob(f):
	blob = 0
	for line in f:
		if "blobs pixels: " in line:
			blobs = line.split("blobs pixels: ")[1].strip()
			blob = blobs.split()[0]
	return blob

def getCB(f):
	min1 = "100"
	min2 = "100"
	max1 = "100"
	max2 = "100"
	lines = f.readlines()
	n = 0
	CB = []
	for line in lines:
		n = n + 1
		if "Capture Checker board" in line:
			min1_ = lines[n+1].split("min")[1]
			min1 = min1_.split()[0]
			max1_ = lines[n+1].split("max")[1]
			max1 = max1_.split()[0]
			min2_ = lines[n+2].split("min")[1]
			min2 = min2_.split()[0]
			max2_ = lines[n+2].split("max")[1]
			max2 = max2_.split()[0]
			CB = min1 + "~" + max1 + "/" + min2 + "~" + max2
			continue
	return CB

def getICB(f):
	min3 = "100"
	min4 = "100"
	max3 = "100"
	max4 = "100"
	newf = f.readlines()
	m = 0
	ICB = []
	for line in newf:
		m = m + 1
		if "Capture Inverted Checker board" in line:
			min3_ = newf[m+1].split("min")[1]
			min3 = min3_.split()[0]
			max3_ = newf[m+1].split("max")[1]
			max3 = max3_.split()[0]
			min4_ = newf[m+2].split("min")[1]
			min4 = min4_.split()[0]
			max4_ = newf[m+2].split("max")[1]
			max4 = max4_.split()[0]
			ICB = min3 + "~" + max3 + "/" + min4 + "~" + max4
			continue
	return ICB

def CB_deadpixel(f):
	CBDP = 0
	CB = f.readlines()
	a = 0
	for lineCB in CB:
		a = a + 1
		if "Capture Checker board" in lineCB:
			CBDP_ = CB[a+3].split("pixels:")[1].strip()
			CBDP = CBDP_.split()[0]
			continue
	return CBDP

def ICB_deadpixel(f):
	ICBDP = 0
	ICB = f.readlines()
	b = 0
	for lineICB in ICB:
		b = b + 1
		if "Capture Inverted Checker board" in lineICB:
			ICBDP_ = ICB[b+3].split("pixels:")[1].strip()
			ICBDP = ICBDP_.split()[0]
			continue
	return ICBDP

def run(rootdir):
	for dir, subdir, filenames in os.walk(rootdir):
		for filename in filenames:
			if fnmatch.fnmatch(filename, "*_log.txt"):
				logfile = os.path.join(dir, filename)
				logfiles.append(logfile)

	filename = xlwt.Workbook()
	sheet = filename.add_sheet("my_sheet")
	row = 1
	sheet.write(0,0,"file name")
	sheet.write(0,1,"Signal Strength")
	sheet.write(0,2,"Uniformity")
	sheet.write(0,3,"Blob NO.")
	sheet.write(0,4,"Check Board")
	sheet.write(0,5,"Inverted Check Board")
	sheet.write(0,6,"CB_deadpixel")
	sheet.write(0,7,"ICB_deadpixel")

	for file in logfiles:
		col = 0
		sheet.write(row,col,file)
		with open(file) as f:
			col = 1
			sheet.write(row,col,getSS(f))
		with open(file) as f:
			col = 2
			sheet.write(row,col,getUnif(f))
		with open(file) as f:
			col = 3
			sheet.write(row,col,getBlob(f))
		with open(file) as f:
			col = 4
			sheet.write(row,col,getCB(f))
		with open(file) as f:
			col = 5
			sheet.write(row,col,getICB(f))
		with open(file) as f:
			col = 6
			sheet.write(row,col,CB_deadpixel(f))
		with open(file) as f:
			col = 7
			sheet.write(row,col,ICB_deadpixel(f))
		row = row + 1


	filename.save("Capacitance.xls")

	print ("{} files processed...".format(len(logfiles)))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		run(sys.argv[1])
	else:
		print("python Capacitance_results_extract.py <directory>")


				
