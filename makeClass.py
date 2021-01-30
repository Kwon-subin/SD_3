import ESGuide as es
from flask import Flask, Blueprint
from flask import render_template, redirect, url_for
from flask import request, session
from werkzeug.utils import secure_filename
import sys
import re
import operator
import time

from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

bp_makeClass = Blueprint('makeClass', __name__)
bp_makeClass.secret_key = "SD_3"

CLASS_NUM = "0000"


def get_cn():
    global CLASS_NUM

    doc = es.get_doc('class_num', 'class_num')
    if doc == -1:
        CLASS_NUM = "{:>04d}".format(0)
    else:
        CLASS_NUM = doc['_source']['CLASS_NUM']

    return CLASS_NUM


def update_cn():
    es.insert_doc('class_num', 'class_num', {'CLASS_NUM' : CLASS_NUM})



@bp_makeClass.route('/')
def main():
    #if session['T'] == "True":
    return render_template("buttonClass.html")
    #else:
        #return render_template("register_f.html") #수강생 신분이면 오류 발생

@bp_makeClass.route('/buttonClass', methods=['GET'])
def buttonClass():
    b_category = request.args.get('b_category')
    s_category = request.args.get('s_category')

    return render_template("makeClass.html", b_category = b_category, s_category = s_category)

@bp_makeClass.route('/makeClass', methods=['POST'])
def makeClass():
    if request.method == 'POST':
        y_str = str(datetime.today().year) #현재 연도
        m_str = str(datetime.today().month) #현재 월
        d_str = str(datetime.today().day) #현재 일
        h_str = str(datetime.now().hour) #현재 시
        min_str = str(datetime.now().minute) #현재 월
        cost_str = request.form['cost']
        c_name = request.form['c_name']
        cat_name = request.form['cat_name']
        cat_detail = request.form['cat_detail']
        c_content = request.form['content']
        meet_str = str(request.form.get('m'))
        when = y_str + '-' + m_str + '-' + d_str + '/' + h_str + ':' + min_str
        start = request.form['start']
        end = request.form['end']
        cost = int(cost_str)
        ID = session['user_id']

        global CLASS_NUM
        get_cn()
    
        if meet_str == "offline":
            M = True
        if meet_str == "online":
            M = False

        i_class = {
            'ID' : ID,
            'c_name' : c_name,
            'cost' : cost,
            'start' : start, #YYYY-MM-DD/
            'end' : end,
            'M' : M, #Meet, Offline > True, Online > False
            'c_content' : c_content,
            #'cat_name' : cat_name,
            #'cat_detail' : cat_detail,
        }
        res = es.insert_doc('class', CLASS_NUM,i_class)
        es.addToCategory(cat_name, cat_detail, 'class', CLASS_NUM)
        cn = int(CLASS_NUM) + 1
        if(cn > 9999):
            return -1
        CLASS_NUM = "{:>04d}".format(cn)
        update_cn()


        return render_template('confirmClass.html', b_category=cat_name, s_category=cat_detail, _class=i_class)

if __name__ == '__main__':
    bp_makeClass.run(host='127.0.0.1', port=5000, debug=True)
