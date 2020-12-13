import community_base as cb
from flask import Flask, render_template, request, redirect, url_for, session
import string
import random




string_pool = string.ascii_letters + string.digits + string.punctuation
key = ""
for i in range(10):
    key += random.choice(string_pool)
app = Flask(__name__)
app.secret_key = key

CATEGORIES = ['test1', 'test2']




########### 로그인 ###########

@app.route('/')
def main():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    ID = request.form['ID']
    session['user_id'] = ID

    return redirect(url_for('community', category = 'None', page = 0))




########### 페이지 관련 ###########

@app.route('/community', methods=['GET'])
def community():
    ID = session.get('user_id')
    category = request.args.get('category')
    page = int(request.args.get('page'))
    docs, hots, page = cb.show(category, page)

    return render_template('community.html', categories = CATEGORIES, hots = hots, posts = docs, ID = ID, category = category, page = page)


@app.route('/nextpage', methods=['POST'])
def nextpage():
    category = request.form['category']
    page = int(request.form['page'])
    page = cb.next_page(page)

    return redirect(url_for('community', category = category, page = page))


@app.route('/backpage', methods=['POST'])
def backpage():
    category = request.form['category']
    page = int(request.form['page'])
    page = cb.back_page(page)

    return redirect(url_for('community', category = category, page = page))




########### 글쓰기 ###########

@app.route('/post', methods=['POST'])
def post():
    ID = session.get('user_id')
    category = request.form['category']

    return render_template('post.html', ID = ID, categories = CATEGORIES, category = category)

@app.route('/posting', methods=['POST'])
def posting():
    ID = session.get('user_id')
    title = request.form['title']
    content = request.form['content']
    hashtags = request.form['hashtags']
    category = request.form['category']
    
    cb.post(ID, title, content, hashtags, category)


    return redirect(url_for('community', category = category, page = 0))




########### 글읽기 ###########

@app.route('/read', methods=['POST'])
def read():
    ID = session.get('user_id')
    post_id = request.form['post_id']
    page = int(request.form['page'])
    category = request.form['category']
    post = cb.read(post_id)


    return render_template('read.html', reading = post, login = ID, page = page, category = category)
    



@app.route('/recommend', methods=['POST'])
def recommend():
    post_id = request.form['post_id']
    no = cb.recommend(post_id)

    return redirect(url_for('read'), code = 307)




@app.route('/report', methods=['POST'])
def report():
    post_id = request.form['post_id']
    no = cb.report(post_id)

    return redirect(url_for('read'), code = 307)




@app.route('/revise', methods=['POST'])
def revise():
    ID = session.get('user_id')
    post_id = request.form['post_id']
    page = int(request.form['page'])
    category = request.form['category']
    post = cb.read(post_id)

    return render_template('revise.html', ID = ID, reading = post, page = page, post_id = post_id, categories = CATEGORIES, category = category)




@app.route('/revising', methods=['POST'])
def revising():
    post_id = request.form['post_id']
    page = int(request.form['page'])
    title = request.form['title']
    content = request.form['content']
    hashtags = request.form['hashtags']
    originalC = request.form['originalC']
    category = request.form['category']
    
    no = cb.revise(post_id, title, content, hashtags, originalC, category)


    return redirect(url_for('read'), code = 307)




@app.route('/delete', methods=['POST'])
def delete():
    post_id = request.form['post_id']
    category = request.form['category']
    page = int(request.form['page'])
    cb.delete(post_id, category)

    return redirect(url_for('community', category = category, page = page))




########### 댓글 관련 ###########

@app.route('/reply', methods=['POST'])
def reply():
    ID = session.get('user_id')
    content = request.form['content']
    post_id = request.form['post_id']
    no = cb.reply(post_id, ID, content)
    page = int(request.form['page'])


    return redirect(url_for('read'), code = 307)




@app.route('/reply_report', methods=['POST'])
def reply_report():
    reply_id = request.form['reply_id']
    
    no = cb.reply_report(reply_id)
    page = int(request.form['page'])


    return redirect(url_for('read'), code = 307)




@app.route('/reply_revise', methods=['POST'])
def reply_revise():
    reply_id = request.form['reply_id']
    content = request.form['content']
    page = int(request.form['page'])

    no = cb.reply_revise(reply_id, content)


    return redirect(url_for('read'), code = 307)




@app.route('/reply_delete', methods=['POST'])
def reply_delete():
    reply_id = request.form['reply_id']

    no = cb.reply_delete(reply_id)
    page = int(request.form['page'])


    return redirect(url_for('read'), code = 307)




########### 검색 ###########

@app.route('/search', methods=['POST'])
def search():
    ID = session.get('user_id')
    condition = request.form['condition']
    
    docs = cb.search(condition)
    if docs == -1:
        docs = {}


    return render_template('community.html', categories = CATEGORIES, category = 'None', posts = docs, page = 0, ID = ID)




if __name__ == '__main__':
    app.run()
    #app.run(host = '0.0.0.0')