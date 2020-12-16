import ESGuide as es
from flask import Blueprint
from flask import render_template
from flask import request, session
from flask import redirect, url_for
from werkzeug.utils import secure_filename
import sys
import re
import operator
import time

from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

bp_login = Blueprint('login', __name__)
bp_login.secret_key = "SD_3"

@bp_login.route('/')
def main():
    return render_template("login.html")

@bp_login.route('/choose/student', methods=['get'])
def choose_register():
    return render_template("register_student.html")

@bp_login.route('/choose/teacher', methods=['get'])
def choose_teacher():
    return render_template("register_teacher.html")

@bp_login.route('/register/student', methods=['POST'])
def register_student():
    if request.method == 'POST':
        T_data = False
        id = request.form['member_id']
        y_str = request.form['year']
        m_str = request.form['month']
        d_str = request.form['day']
        birth_str = y_str + '-' + m_str + "-" + d_str
        n = int(y_str)
        today_y = datetime.today().year
        today_m = datetime.today().month
        today_d = datetime.today().day
        age = today_y - n
        return_m = today_m - int(m_str)
        if return_m > 0:
            age = age + 1
        if return_m == 0:
            return_d = today_d - int(d_str)
            if return_d >= 0:
                age = age+1

        #accountDic['age'] = age
        f_phone = request.form['f_phone']
        s_phone = request.form['s_phone']
        t_phone = request.form['t_phone']
        phone = f_phone + '-' + s_phone + '-' + t_phone
        accountDic = {
            'PW' : request.form['passwd'],
            'name' : request.form['name'],
            'age' : age, #만나이로 통일
            'birth' : birth_str, #YYYYMMDD
            'phone' :  phone, #'-'포함
            'T' : False, #Teacher, Teacher > True, Student > False
            'class' : []
        }
        res = es.get_doc('account', id)
        if res == -1:
            res2 = es.insert_doc('account' ,id, accountDic)
            return render_template('login.html')

        else:
            return render_template('register_student.html')


@bp_login.route('/register/teacher', methods=['POST'])
def register_teacher():
    if request.method == "POST":
        T_data = True
        id = request.form['member_id']
        y_str = request.form['year']
        m_str = request.form['month']
        d_str = request.form['day']
        birth_str = y_str + '-' + m_str + "-" + d_str
        n = int(y_str)
        today_y = datetime.today().year
        today_m = datetime.today().month
        today_d = datetime.today().day
        age = today_y - n
        return_m = today_m - int(m_str)
        if return_m > 0:
            age = age + 1
        if return_m == 0:
            return_d = today_d - int(d_str)
            if return_d >= 0:
                age = age+1
            #accountDic['age'] = age
        f_phone = request.form['f_phone']
        s_phone = request.form['s_phone']
        t_phone = request.form['t_phone']
        phone = f_phone + '-' + s_phone + '-' + t_phone
        accountDic = {
            'PW' : request.form['passwd'],
            'name' : request.form['name'],
            'age' : age, #만나이로 통일
            'birth' : birth_str, #YYYYMMDD
            'phone' :  phone, #'-'포함
            'T' : True, #Teacher, Teacher > True, Student > False
            'class' : []
        }
        cer = request.form['certificate_num']
        cer_num = int(cer)
        place = request.form['place']
        teacher = {
            'certificate_num' : cer_num,
            'place' : place #OOO도 OO시 / OOOO시
        }
        res = es.get_doc('account', id)
        if res == -1:
            res2 = es.insert_doc('account' ,id, accountDic)
            res3 = es.insert_doc('teacher', id, teacher)
            return render_template('login.html')
        else: #있는 아이디 인 경우
            return render_template('register_teacher.html')

@bp_login.route('/login_input', methods=['POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_password = request.form['user_password']
        res = es.get_doc('account', user_id)
        if res == -1:
            return render_template('login.html')
        else:
            if res['_source']['PW'] == user_password:
                session['user_id'] = user_id
                session['name'] = res['_source']['name']
                session['T'] = res['_source']['T']
                session['class'] = res['_source']['class']
                return redirect(url_for('class.main_class'))
            else:
                return render_template('login.html')

if __name__ == '__main__':
    bp_login.run(host='127.0.0.1', port=5000, debug=True)
