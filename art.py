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
import re

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
		d = show_art(path+'arts/'+f)
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
	
def code_trans(d, langs):
	flag = False
	nd = d.split('\r\n')
	for i in range(len(nd)):
		if flag:
			if re.match(r'^```\s*', nd[i]):
				#add tag to langs array
				nd[i] = ''
				flag = False
				continue
			nd[i] = '\t' + nd[i]
			continue
		if re.match(r'^```\s*', nd[i]):
			nd[i] = ''
			flag = True	
	return '\r\n'.join(nd)
	
def show_art(fn):
	try:
		with codecs.open(fn, 'r', encoding='utf-8') as f:
			data = f.read()
			d = json.loads(data)
			if checkArtData(d) == False:
				return None
			langs = []
			d['content'] = code_trans(d['content'], langs)
			#make tag to html use from langs array
			d['markdown'] = markdown(d['content'], output_format='HTML5')
			return d
	except:
		print('read file ' + fn + ' error')