#!/usr/bin/env python3
# coding: utf-8
# author: c00c

from flask import Flask, request
import time, json, codecs
from urllib.parse import quote
import os
from art import loadArt, writeArt, del_art
from jinja2 import Environment, FileSystemLoader
from make import make

app = Flask(__name__)
cwd = os.path.split(os.path.realpath(__file__))[0] + '/'
env = Environment(loader = FileSystemLoader(cwd))
template = env.get_template('edit.htm')

@app.route('/', methods=['GET'])
def home():
	with codecs.open(cwd+'index.html', 'r', 'utf_8') as f:
		d = f.read()
		d += "<script>$('.title-label').each(function(){$(this).after(\"<a class='am-icon-edit' 	style='font-size:16px;opacity:0.9;margin-left: 5px;' href='edit?k=\"+$(this).attr('k')+\"'></a><a class='am-icon-remove' style='font-size:18px;opacity:0.9;margin-left: 5px;' href='delete?k=\"+$(this).attr('k')+\"'></a>\")});$('#contents').append(\"<div style='text-align:center;'><a class='am-btn am-btn-primary am-icon-plus' href='write'>写文章</a></div>\")</script>"
		return d

@app.route('/edit', methods=['GET'])
def editGET():
	k = request.args.get('k', '')
	if k:
		d = loadArt(cwd+'arts/'+k+'.json')
		return template.render(art=d, key=k)
	else:
		return 'arguements error'

@app.route('/edit', methods=['POST'])
def editPOST():
	d = {
		'title': request.form['title'],
		'tags': request.form['tags'],
		'content': request.form['input']
	}
	fn = cwd + 'arts/' + request.form['k'] + '.json'
	if writeArt(d, file_path=fn) == True:
		make()
		return '<script>alert("edit ok");</script>'
	else:
		return 'edit failed'

@app.route('/write', methods=['GET'])
def writeGET():
	with open(cwd+'write.htm','rt') as f:
		return f.read()

@app.route('/write', methods=['POST'])
def writePOST():
	d = {
		'title': request.form['title'],
		'tags': request.form['tags'],
		'content': request.form['input']
	}
	t = str(int(time.time()))
	if writeArt(d, file_path = cwd+'/arts/'+t+'.json'):
		make()
		return '<script>alert("写入成功");location.href="/";</script>'
	return '写入失败'
	
@app.route('/delete', methods=['GET'])
def deleteGET():
	k = request.args.get('k', '')
	if k:
		del_art(k,base_path = cwd)
		make()
		return '<script>alert("删除成功");location.href="/";</script>'
	else:
		return 'arguements error'
	
@app.route('/<id>.html', methods=['GET'])
def artGET(id):
	with codecs.open(cwd+id+'.html','r','utf-8') as f:
		return f.read()
		
@app.route('/about.htm', methods=['GET'])
def aboutGET():
	with open(cwd+'about.htm','rt') as f:
		return f.read()

if __name__ == '__main__':
    app.run(port=80)
