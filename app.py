#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: vap0r
# github: github.com/qq53

from flask import Flask, request
import codecs, time, json
from urllib.parse import quote

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
	with codecs.open('write.htm','r','utf-8') as f:
		return f.read()

@app.route('/', methods=['POST'])
def write():
	fn = str(int(time.time())) + '.json'
	d = {
	'title': request.form['title'],
	'tags': request.form['tags'],
	'content': request.form['input'].replace('\r\n','<br />')
	}
	with codecs.open('arts/'+fn,'w','utf-8') as f:
		f.write(json.dumps(d))
		return '<script>alert("写入成功");location.href="/";</script>'
	return '写入失败'

if __name__ == '__main__':
    app.run()