#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
import os
import codecs
import markdown

env = Environment(loader = FileSystemLoader('templates'))
template = env.get_template('index.html')
ds = []
ds.append({
	'title':'加密算法总结',
	'tags':('tag1','tag2'),
        'year':2015
	})
ds.append({
	'title':'WinHex 14.1 SR-6 爆破',
	'tags':('tag1',)
	})
ds.append({
	'title':'西普学院 – 逆向 – 此处无声',
	'tags':('tag1','tag2'),
        'year':2014
	})

css_list = ('sidebar',)

u = 'http://blog.vap0r.cn'

with codecs.open('templates\\tmp.html', 'w', 'utf-8') as f:
    f.write(template.render(arts=ds, css=css_list, index=u))

html = markdown.markdown('#title')
print(html)
	
exit()
