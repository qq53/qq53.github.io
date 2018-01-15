#!/usr/bin/env python3
# coding: utf-8
# author: c00c

from jinja2 import Environment, FileSystemLoader
import os, codecs
from art import scan
from clean import cleanDir

def make():
	cwd = os.path.split(os.path.realpath(__file__))[0] + '/'
	cleanDir(cwd, 'html')

	env = Environment(loader = FileSystemLoader(cwd+'templates'))
	template_index = env.get_template('index.html')
	template_single = env.get_template('single.html')

	h = 'c00c.cc'
	t = 'c00c'
	
	arts_list = scan(cwd)

	for a in arts_list:
		with codecs.open(cwd+a['file_name']+'.html', 'w', 'utf_8') as f:
			f.write(template_single.render(art=a, index=h, title=t))

	with codecs.open(cwd+'index.html', 'w', 'utf_8') as f:
		f.write(template_index.render(arts=arts_list, index=h, title=t))

if __name__ == '__main__':
	make()