import ESGuide as es
from flask import Blueprint
from flask import render_template
from flask import request, session, redirect
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

@bp_enroll.route('/')
def main():
    return render_template("confirmClass.html")
    
@bp_enroll.route('/return_class')
def return_c():
    return render_template("confirmClass.html")
    
@bp_enroll.route('/payment')
def enroll():
    return render_template("payment.html")


if __name__ == '__main__':
    bp_enroll.run(host='127.0.0.1', port=5000, debug=False)


