#!/usr/bin/env python3
# coding: utf-8
# author: c00c

from markdown import markdown
import json
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
	finally:
		return True

def writeArt(d, file_path):		
	try:
		with open(file_path, 'w') as f:
			if checkArtData(d) == False:
				return None
			f.write(json.dumps(d))
		return True
	except:
		print('write file ' + fn + ' error')

def del_art(k, base_path):		
	try:
		os.remove(base_path+k+'.html')
		os.remove(base_path+'arts\\'+k+'.json')
	except:
		print('write file ' + fn + ' error')
		
def loadArt(fn):
	try:
		with open(fn, 'rt') as f:
			data = f.read()
			d = json.loads(data)
			if checkArtData(d) == False:
				return None
			d['markdown'] = markdown(d['content'], output_format='HTML5')
			return d
	except:
		print('read file ' + fn + ' error')

def scan(path):
	files = os.listdir(path+'arts\\')
	files = sorted(files,reverse=True)

	now = ''
	lt = []
	for f in files:
		n = f[:f.find('.')]
		t = datetime.fromtimestamp(int(n)).strftime('%Y')
		d = show_art(path+'arts\\'+f)
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

def add_attr(str, attr):
	s = re.search(r'(<[^/<> ]+)', str).group(1)
	spos = str.find(s)
	epos = spos + len(s)
	return str[:epos] + ' ' + attr + str[epos:]
	
def parse(d):
	nd = d.split('\r\n')
	
	code_block = False
	result = ''
	codes = []

	for l in nd:
		if l == '':
			continue
		
		if l[:3] == '```':
			code_block ^= True
			if code_block:
				lang = 'c'
				m = re.match(r'```(\w+)\s*', l)
				if m:
					lang = m.group(1)
				continue
			else:
				tmp = markdown('\r\n'.join(codes), output_format='HTML5').split('\n')
				tmp[0] = add_attr(tmp[0],'class="lang-'+lang+'"')
				result += '\r\n'.join(tmp)
				codes.clear()
				continue
		if code_block:
			codes.append('\t'+l)
			continue

		m = re.match(r'^{(.+)}(.+)$', l)
		if m:
			result += add_attr(markdown(m.group(2), output_format='HTML5'), m.group(1)) + '\r\n'
			continue
			
		result += markdown(l, output_format='HTML5') + '\r\n'
			
	#print(json.dumps(result.split('\r\n'),indent=2))
	return result
	
def show_art(fn):
	with open(fn, 'rt') as f:
		data = f.read()
		d = json.loads(data)
		if checkArtData(d) == False:
			return None
		d['markdown'] = parse(d['content'])
		return d