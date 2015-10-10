#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: vap0r
# github: github.com/qq53

import os

def cleanDir(path, type):
	dirs = filter(lambda x: x.find('.'+type)>0,os.listdir(path))
	for d in dirs:
		os.remove(path+'/'+d)
		
if __name__ == '__main__':
	cleanDir('.', 'html')