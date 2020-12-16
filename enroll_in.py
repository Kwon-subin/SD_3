import ESGuide as es
from flask import Blueprint
from flask import render_template
from flask import request, session, redirect, url_for
from werkzeug.utils import secure_filename
import sys
import re
import operator
import time

from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

bp_enroll = Blueprint('enroll', __name__)
bp_enroll.secret_key = "SD_3"


@bp_enroll.route('/enroll', methods=['POST'])
def main():
    class_id = request.form['class_id']
    _class = es.get_doc('class', class_id)
    b_category = request.form['b_category']
    s_category = request.form['s_category']
    ID = session.get('user_id')

    reviews = es.search_dbr_sorted('review', 'id', class_id+"000", class_id+"1000", [{'_id':'desc'}])

    review = session.get('class')
    if review != None:
        if class_id in review:
            review = True
        else:
            review = False
    else:
        review = False

    return render_template("enroll_in.html", class_id = class_id, _class = _class, b_category = b_category, s_category = s_category, reviews = reviews, ID = ID, review = review)
    

@bp_enroll.route('/return_class')
def return_c():
    return render_template("enroll_in.html")
    

@bp_enroll.route('/payment', methods=['POST'])
def enroll():
    class_id = request.form['class_id']
    _class = es.get_doc('class', class_id)
    b_category = request.form['b_category']
    s_category = request.form['s_category']

    try:
        session.get('class')
        session['class'].append(class_id)
    except:
        session['class'] = [class_id]

    return render_template("payment.html", _class = _class, b_category = b_category, s_category = s_category)


@bp_enroll.route('/review', methods=['POST'])
def review():
    content = request.form['review_content']
    rating = request.form['rating']
    class_id = request.form['class_id']

    print(rating)
    ID = session['user_id']
    t = datetime.now()
    time = "{:>04d}-{:>02d}-{:>02d}/{:>02d}:{:>02d}".format(t.year, t.month, t.day, t.hour, t.minute)

    review = {
        'id' : 'String',
        'ID' : ID,
        'content' : content,
        'rate' : rating,
        'time' : time
        }
    
    reviews = es.search_dbr_sorted('review', 'id', class_id+"000", class_id+"1000", [{'_id':'desc'}])

    if reviews == -1:
        review['id'] = class_id + "000"
        n = es.insert_doc('review', class_id+"000", review)

    else:
        _len = len(reviews)
        review_id = "{:>03d}".format(_len)
        review['id'] = class_id + review_id
        n = es.insert_doc('review', class_id+review_id, review)

    
    return redirect(url_for('enroll.main'), code=307)



if __name__ == '__main__':
    bp_enroll.run(host='127.0.0.1', port=5000, debug=False)


