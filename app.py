#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: vap0r
# github: github.com/qq53

from flask import Flask, request
import codecs, time, json
from urllib.parse import quote
import os

app = Flask(__name__)
cwd = os.getcwd() + '/'

@app.route('/', methods=['GET'])
def home():
	with codecs.open(cwd+'index.html','r','utf-8') as f:
		d = f.read().split('\n')
		d[86] += "<script>$('.title-label').each(function(){$(this).after(\"<a class='am-icon-edit' 	style='font-size:16px;vertical-align:middle;opacity:0.9;margin: -4px 0 0 5px;' href='edit.htm?f=\"+$(this).attr('t')+\"'></a>\")});$('#contents').append(\"<div style='text-align:center;'><a class='am-btn am-btn-primary am-icon-plus' href='edit.htm'>写文章</a></div>\")</script>"
		return ''.join(d)

@app.route('/edit', methods=['POST'])
def write():
	fn = str(int(time.time())) + '.json'
	d = {
	'title': request.form['title'],
	'tags': request.form['tags'],
	'content': request.form['input'].replace('\r\n','<br />')
	}
	with codecs.open(cwd+'arts/'+fn,'w','utf-8') as f:
		f.write(json.dumps(d))
		return '<script>alert("写入成功");location.href="/";</script>'
	return '写入失败'

@app.route('/edit', methods=['GET'])
def edit():
	with codecs.open(cwd+'edit.htm','r','utf-8') as f:
		return f.read()

if __name__ == '__main__':
    app.run(port=80)