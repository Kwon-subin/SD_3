import ESGuide as es
from flask import Flask
from flask import render_template
from flask import request, session
from werkzeug.utils import secure_filename
import sys
import re
import requests
import operator
import time

from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

makeClass = Flask(__name__)
makeClass.secret_key = "SD_3"

@makeClass.route('/')
def main():
    #if session['T'] == "True":
    return render_template("buttonClass.html")
    #else:
        #return render_template("register_f.html") #수강생 신분이면 오류 발생

@makeClass.route('/buttonClass')
def buttonClass():
    return render_template("makeClass.html")

@makeClass.route('/makeClass', methods=['POST'])
def makeClass_():
    if request.method == 'POST':
        y_str = str(datetime.today().year) #현재 연도
        m_str = str(datetime.today().month) #현재 월
        d_str = str(datetime.today().day) #현재 일
        h_str = str(datetime.now().hour) #현재 시
        m_str = str(datetime.now().minute) #현재 월
        cost_str = request.form['cost']
        c_name = request.form['c_name']
        cat_name = request.form['cat_name']
        cat_detail = request.form['cat_detail']
        m_str = str(request.form.get('m'))
        when = y_str + '-' + m_str + '-' + d_str + '/' + h_str + ':' + m_str
        cost = int(cost_str)
        #ID = session['user_id']
        ID = "tn1256"
        pid = ID + y_str + m_str + d_str + h_str + m_str #예 : tn125620201127
        if m_str == "offline":
            M = True
        if m_str == "online":
            M = False

        i_class = {
            'ID' : ID,
            'c_name' : c_name,
            'cost' : cost,
            'when' : when, #YYYY-MM-DD/HH:MM (시간은 24시간 단위)
            'M' : M, #Meet, Offline > True, Online > False
            #'cat_name' : cat_name,
            #'cat_detail' : cat_detail,
        }
        res = es.insert_doc('class',pid,i_class)
        if res == -1:
            return render_template("register_f.html")
        else:
            return render_template("register_s.html")

if __name__ == '__main__':
    makeClass.run(host='127.0.0.1', port=5000, debug=True)
