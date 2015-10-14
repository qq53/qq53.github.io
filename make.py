#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: vap0r
# github: github.com/qq53

from jinja2 import Environment, FileSystemLoader
import os
import codecs
from art import scan
from clean import cleanDir

def make():
	cwd = os.getcwd() + '/'
	cleanDir(cwd, 'html')

	env = Environment(loader = FileSystemLoader(cwd+'templates'))
	template_index = env.get_template('index.html')
	template_single = env.get_template('single.html')

	u = 'http://blog.vap0r.cn'

	#arts_list = scan()
	art = {
	'title':'1',
	'tags':'2',
	'content':'test',
	'file_name':'1'
	}
	arts_list = []
	arts_list.append(art)

	for a in arts_list:
		with codecs.open(cwd+a['file_name']+'.html', 'w', 'utf-8') as f:
			f.write(template_single.render(art=a, index=u))

	with codecs.open(cwd+'index.html', 'w', 'utf-8') as f:
		f.write(template_index.render(arts=arts_list, index=u))

if __name__ == '__main__':
	make()