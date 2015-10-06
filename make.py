#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: vap0r
# github: github.com/qq53

from jinja2 import Environment, FileSystemLoader
import os
import codecs
from art import scan

env = Environment(loader = FileSystemLoader('templates'))
template = env.get_template('index.html')


css_list = ('sidebar',)

u = 'http://blog.vap0r.cn'

with codecs.open('templates\\tmp.html', 'w', 'utf-8') as f:
    f.write(template.render(arts=scan(), css=css_list, index=u))
	
exit()