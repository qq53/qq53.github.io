#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import os

env = Environment(loader = FileSystemLoader('templates'))
template = env.get_template('index.html')
ds = []
ds.append({
	'title':'1',
	'contents':'2'
	})
ds.append({
	'title':'3',
	'contents':'4'
	})

with open('tmp.html','wt') as f:
	f.write(template.render(posts=ds))
