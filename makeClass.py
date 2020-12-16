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
        m_str = str(datetime.now().minute) #현재 월
        cost_str = request.form['cost']
        c_name = request.form['c_name']
        cat_name = request.form['cat_name']
        cat_detail = request.form['cat_detail']
        m_str = str(request.form.get('m'))
        when = y_str + '-' + m_str + '-' + d_str + '/' + h_str + ':' + m_str
        start = request.form['start']
        end = request.form['end']
        cost = int(cost_str)
        ID = session['user_id']
        pid = ID + y_str + m_str + d_str + h_str + m_str #예 : tn125620201127
        if m_str == "offline":
            M = True
        if m_str == "online":
            M = False

        i_class = {
            'ID' : ID,
            'c_name' : c_name,
            'cost' : cost,
            'start' : start, #YYYY-MM-DD/HH:MM (시간은 24시간 단위)
            'end' : end
            'M' : M, #Meet, Offline > True, Online > False
            #'cat_name' : cat_name,
            #'cat_detail' : cat_detail,
        }
        res = es.insert_doc('class',pid,i_class)
        es.addToCategory(cat_name, cat_detail, 'class', pid)
        return redirect(url_for('class.'+cat_name+'_'+cat_detail))

if __name__ == '__main__':
    bp_makeClass.run(host='127.0.0.1', port=5000, debug=True)
