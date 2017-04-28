#!/usr/bin/env python3
# coding: utf8
# author: c00c

import os

def cleanDir(path, type):
	dirs = filter(lambda x: x.find('.'+type)>0,os.listdir(path))
	for d in dirs:
		os.remove(path+'/'+d)
		
if __name__ == '__main__':
	cwd = os.path.split(os.path.realpath(__file__))[0] + '/'
	cleanDir(cwd, 'html')