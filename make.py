#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import os

env = Environment(loader = FileSystemLoader('templates'))
template = env.get_template('index.html')
print(template.render(str='11'))
