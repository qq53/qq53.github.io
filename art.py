#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: vap0r
# github: github.com/qq53

from markdown import markdown
import json
import codecs
import time
from datetime import datetime
import os
from urllib.parse import unquote

def checkArtData(data):
	try:
		data['title'] and data['tags'] and data['content']
	except:
		print('Error article data format, must have ["title", "tags", "content"]')
		return False
	else:
		return True

def loadArt(fn):
	try:
		with codecs.open('arts/' + fn + '.json', 'r', encoding='utf-8') as f:
			data = f.read()
			d = json.loads(data)
			if checkArtData(d) == False:
				return None
			d['content'] = unquote(d['content'])
			d['content'] = markdown(d['content'], output_format='HTML5')
			return d
	except:
		print('read file ' + fn + ' error')

def scan():
	files = os.listdir('arts')
	files = sorted(files)
	
	now = ''
	lt = []
	for f in files:
		n = f[:f.find('.')]
		t = datetime.fromtimestamp(int(n)).strftime('%Y')
		d = loadArt(n)
		if not d:
			return None
		d['date'] = datetime.fromtimestamp(int(n)).strftime('%Y/%m/%d')
		d['file_name'] = n
		if now != t:
			now = t
			d['year'] = now
		lt.append(d)
	return lt
