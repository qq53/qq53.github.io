#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: vap0r
# github: github.com/qq53

from markdown import markdown
import json
import codecs
from datetime import datetime
import os
import time

def checkArtData(data):
	try:
		data['title'] and data['tags'] and data['content']
	except:
		print('Error article data format, must have ["title", "tags", "content"]')
		return False
	else:
		return True

def writeArt(d, file_path):		
	try:
		with codecs.open(file_path, 'w', encoding='utf-8') as f:
			if checkArtData(d) == False:
				return None
			f.write(json.dumps(d))
		return True
	except:
		print('write file ' + fn + ' error')

def loadArt(fn):
	try:
		with codecs.open(fn, 'r', encoding='utf-8') as f:
			data = f.read()
			d = json.loads(data)
			if checkArtData(d) == False:
				return None
			d['markdown'] = markdown(d['content'], output_format='HTML5')
			return d
	except:
		print('read file ' + fn + ' error')

def scan(path):
	files = os.listdir(path+'arts/')
	files = sorted(files)
	
	now = ''
	lt = []
	for f in files:
		n = f[:f.find('.')]
		t = datetime.fromtimestamp(int(n)).strftime('%Y')
		d = loadArt(path+'arts/'+f)
		if not d:
			return None
		d['date'] = datetime.fromtimestamp(int(n)).strftime('%Y/%m/%d')
		d['file_name'] = n
		d['tags'] = d['tags'].split(' ')
		if now != t:
			now = t
			d['year'] = now
		lt.append(d)
	return lt