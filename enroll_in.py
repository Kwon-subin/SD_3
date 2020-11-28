import ESGuide as es
from flask import Flask
from flask import render_template
from flask import request, session, redirect
from werkzeug.utils import secure_filename
import sys
import re
import requests
import operator
import time

from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

app = Flask(__name__)
app.secret_key = "SD_3"

@app.route('/')
def main():
    return render_template("enroll_in.html")
    
@app.route('/return_c')
def return_c():
    return render_template("enroll_in.html")
    
@app.route('/enroll')
def enroll():
    return render_template("payment.html")


@app.route('/payment')
def payment():
    #결제 성공시
    return render_template("enroll_success.html")
    #결제 실패시
    #return render_template("payment_fail.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)


