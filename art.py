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
	
append_arr = []
code_space_fix = 0
	
def code_trans(nd):
	flag = False
	fix = 0
	global code_space_fix
	for i in range(len(nd)):
		if nd[i] == '':
			fix += 1
			continue
		if flag:
			if re.match(r'^```\s*', nd[i]):
				nd[i] = ''
				flag = False
				continue
			nd[i] = '\t' + nd[i]
		else:
			#head
			m = re.match(r'^```(\w+)?\s*', nd[i])
			if m:
				nd[i] = ''
				flag = True	
				if m.groups():
					append_arr.append( {'l':i-fix,'tag':'class="lang-'+m.group(1)+'"'} )
				code_space_fix += 1
	return nd

def before_mark(d):
	nd = d.split('\r\n')
	nd = code_trans(nd)
	fix = 0
	global code_space_fix
	for i in range(len(nd)):
		if nd[i] == '':
			fix += 1
			continue
		m = re.match(r'^{(.+)}(.+)$', nd[i])
		if m:
			nd[i] = m.group(2)
			append_arr.append( {'l':i-fix+code_space_fix,'tag':m.group(1)} )
	return '\r\n'.join(nd)
	
def after_mark(d):
	nd = d.split('\n')
	for di in append_arr:
		sou = nd[di['l']]
		s = re.findall(r'.*<[^/]+?', sou)[0]
		spos = sou.find(s)
		epos = spos + len(s)
		sou = sou[spos:epos] + ' ' + di['tag'] + sou[epos:]
		nd[di['l']] = sou
	return '\n'.join(nd)
	
def show_art(fn):
	try:
		with codecs.open(fn, 'r', encoding='utf-8') as f:
			data = f.read()
			d = json.loads(data)
			if checkArtData(d) == False:
				return None
			global append_arr
			global code_space_fix
			append_arr = []
			code_space_fix = 0
			d['content'] = before_mark(d['content'])
			#print(append_arr)
			d['markdown'] = markdown(d['content'], output_format='HTML5')					
			d['markdown'] = after_mark(d['markdown'])
			return d
	except:
		print('read file ' + fn + ' error')