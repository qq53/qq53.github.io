#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: vap0r
# github: github.com/qq53

from jinja2 import Environment, FileSystemLoader
import os
import codecs
from art import scan

dirs = filter(lambda x: x.find('.html')>0,os.listdir())
for d in dirs:
	os.remove(d)

env = Environment(loader = FileSystemLoader('templates'))
template_index = env.get_template('index.html')
template_single = env.get_template('single.html')

u = 'http://blog.vap0r.cn'

arts_list = scan()

for a in arts_list:
	with codecs.open(a['file_name']+'.html', 'w', 'utf-8') as f:
		f.write(template_single.render(art=a, index=u))

with codecs.open('index.html', 'w', 'utf-8') as f:
    f.write(template_index.render(arts=arts_list, index=u))
	

