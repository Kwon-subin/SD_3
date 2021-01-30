import ESGuide as es
from flask import Flask, render_template, redirect, url_for, session
from community import bp_community
from main_category import bp_class
from register_login import bp_login
from enroll_in import bp_enroll
from makeClass import bp_makeClass




bps = [bp_community, bp_class, bp_login, bp_enroll, bp_makeClass]
app = Flask(__name__)
app.secret_key = 'SD3'




@app.route('/')
def main():
    return render_template('login.html')




@app.route('/logout')
def logout():
    acc = es.get_doc('account', session['user_id'])
    acc['_source']['class'] = session['class']
    es.insert_doc('account', acc['_id'], acc['_source'])

    session.clear()

    return render_template('login.html')




if __name__ == '__main__':
    
    for bp in bps:
        app.register_blueprint(bp)
    
    app.run(host='0.0.0.0', port = 5000, debug = True)
    