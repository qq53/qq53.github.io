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

def checkArtData(data):
	try:
		data['title'] and data['tags'] and data['content']
	except:
		print('Error article data format, must have ["title", "tags", "content"]')
		return False
	else:
		return True

def writeArt(data):
	if checkArtData(data) == False:
		return
	fn = 'arts/' + str(int(time.time())) + '.json'
	jdata = json.dumps(data)
	with codecs.open(fn, 'w', encoding='utf-8') as f:
		f.write(jdata)
	
def loadArt(fn):
	try:
		with codecs.open('arts/' + fn + '.json', 'r', encoding='utf-8') as f:
			data = f.read()
			d = json.loads(data)
			if checkArtData(d) == False:
				return None			
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
		if now != t:
			now = t
			d['year'] = now
		lt.append(d)
	return lt

print(scan())