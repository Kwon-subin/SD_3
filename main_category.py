from flask import Flask, render_template, request
from random import choice

web_site = Flask(__name__)

number_list = [
	100, 101, 200, 201, 202, 204, 206, 207, 300, 301, 302, 303, 304, 305, 307, 400, 401, 402, 403, 404, 405, 406, 408, 409, 410, 411, 412, 413, 414, 415,
	416, 417, 418, 421, 422, 423, 424, 425, 426,
	429, 431, 444, 450, 451, 500, 502, 503, 504, 506, 507, 508, 509, 510, 511, 599
]



#category
@web_site.route('/')
def catelarge():
  return render_template('category.html', code=choice(number_list))

@web_site.route('/catasmall1')
def catesmall1():
  return render_template('catesmall1.html', code=choice(number_list))

@web_site.route('/catasmall2')
def catesmall2():
  return render_template('/catesmall2.html', code=choice(number_list))

@web_site.route('/catasmall3')
def catesmall3():
  return render_template('catesmall3.html', code=choice(number_list))

@web_site.route('/catasmall4')
def catesmall4():
  return render_template('catesmall4.html', code=choice(number_list))

web_site.run(host='0.0.0.0', port=8080)