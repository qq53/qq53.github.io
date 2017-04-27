#!/usr/bin/env python3
# coding: utf8
# author: vap0r
# github: github.com/qq53

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
	
append_arr = []
	
def code_trans(nd):
	fix = 0
	code_fix = 0
	in_code_block = False
	
	for i in range(len(nd)):
		if nd[i] == '':
			fix += 1
			continue
		if in_code_block:
			if re.match(r'^```\s*', nd[i]):
				in_code_block = False
				continue
			nd[i] = '\t' + nd[i]
		else:
			#head
			#if len(m) > 0:
			if nd[i][:3] == '```':
				in_code_block = True
				m = re.findall(r'^```(\w+)?\s*', nd[i])	
				nd[i] = ''
				if len(m) > 0:
					append_arr.append( {'l':i-fix-code_fix,'tag':'class="lang-'+m[0]+'"'} )
				code_fix += 1
				
	return nd

def before_mark(d):
	nd = d.split('\r\n')
	nd = code_trans(nd)
	fix = 0
	code_fix = 0

	#print(json.dumps(nd,indent=2))
	for i in range(len(nd)):
		if nd[i] == '```':
			nd[i] = ''
			code_fix += 1
		if nd[i] == '':
			fix += 1
			continue
		m = re.match(r'^{(.+)}(.+)$', nd[i])
		if m:
			nd[i] = m.group(2)
			append_arr.append( {'l':i-fix+code_fix,'tag':m.group(1)} )
	return '\r\n'.join(nd)
	
def after_mark(d):
	nd = d.split('\n')
	#print(json.dumps(nd,indent=2))
	print(append_arr,len(nd))
	for di in append_arr:
		sou = nd[di['l']]
		print(sou)
		s = re.findall(r'<[^/<> ]+', sou)[0]
		spos = sou.find(s)
		epos = spos + len(s)
		sou = sou[spos:epos] + ' ' + di['tag'] + sou[epos:]
		nd[di['l']] = sou
		print(sou)
	return '\n'.join(nd)
	
def show_art(fn):
	try:
		with open(fn, 'rt') as f:
			data = f.read()
			d = json.loads(data)
			if checkArtData(d) == False:
				return None
			global append_arr
			append_arr = []
			d['content'] = before_mark(d['content'])
			d['markdown'] = markdown(d['content'], output_format='HTML5')
			d['markdown'] = after_mark(d['markdown'])
			return d
	except:
		print('read file ' + fn + ' error')