import ESGuide as es
from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename
import sys
import re
import requests
import operator
import time

from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

register = Flask(__name__)

@register.route('/')
def register_page():
    return render_template("register_page.html", parsed_page=html)

@register.route('./info_insert', methods=['POST'])
def info_insert():
    if request.method == 'POST':
        #myname = request.from['name']
        accountDic = {'id','pw','name','age','birht','phone','T'}
        T_data = True
        id = request.form['member_id']
        accountDic[id] = id
        accountDic[pw] = request.form['passwd']
        acoountDic[name] = request.form['name']
        y_str = request.form['year']
        m_str = request.form['month']
        d_str = request.form['day']
        birth_str = y_str + m_str + d_str
        accountDic[birth] = birth_str
        accountDic[phone] = request.form['phone']

        T_str = request.form['T']
        if T_str == 'True':
            T_data = True
        else:
            T_data = False
        accountDic[T] = T_data

        #y_int = int(y_str)
        #m_int = int(m_str)
        today_y = datetime.today().year
        today_m = datetime.today().month
        today_d = datetime.today().day
        age = today_y - y_str
        if (today_m - m_str) > 0:
            age = age + 1
        if (today_m - m_str) == 0:
            if (today_d - d_str) >= 0:
                age = age+1

        accountDic[age] = age

        res = es.get_idx('account', id)
        if res == -1:
            res2 = es.insert_doc('account' ,id, accountDic)
            if res2 == 0:
                return render_template('register_s.html')
            else: #디버깅
                return render_template('register_f.html')
                #return render_template('register_page.html')
        else:
            return render_template('register_page.html')

if __name__ == '__main__':
    register.run(host='127.0.0.1', port=5000, debug=True)
