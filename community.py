import community_base as cb
from flask import Flask, render_template, request, redirect, url_for, session




app = Flask(__name__)

READING_SIZE = 3




########### 로그인 ###########

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    ID = request.form['ID']
    cb.set_reading_size(READING_SIZE)

    return redirect(url_for('community', page = 0), code = 307)




########### 페이지 관련 ###########

@app.route('/community', methods=['POST'])
def community():
    ID = request.form['ID']
    page = int(request.args.get('page'))
    docs, page = cb.show(page)
    
    return render_template('community.html', posts = docs, ID = ID, page = page)


@app.route('/nextpage', methods=['POST'])
def nextpage():
    ID = request.form['ID']
    page = int(request.form['page'])
    page = cb.next_page(page)

    return redirect(url_for('community', page = page), code = 307)


@app.route('/backpage', methods=['POST'])
def backpage():
    ID = request.form['ID']
    page = int(request.form['page'])
    page = cb.back_page(page)

    return redirect(url_for('community', page = page), code = 307)




########### 글쓰기 ###########

@app.route('/post', methods=['POST'])
def post():
    ID = request.form['ID']

    return render_template('post.html', ID = ID)

@app.route('/posting', methods=['POST'])
def posting():
    ID = request.form['ID']
    title = request.form['title']
    content = request.form['content']
    hashtags = request.form['hashtags']
    
    cb.post(ID, title, content, hashtags)


    return redirect(url_for('community', page = 0), code = 307)




########### 글읽기 ###########

@app.route('/read', methods=['POST'])
def read():
    ID = request.form['ID']
    post_id = request.form['post_id']
    page = int(request.form['page'])
    post = cb.read(post_id)


    return render_template('read.html', reading = post, login = ID, page = page)
    



@app.route('/recommend', methods=['POST'])
def recommend():
    ID = request.form['ID']
    post_id = request.form['post_id']
    no = cb.recommend(post_id)
    page = int(request.form['page'])

    return redirect(url_for('read'), code = 307)




@app.route('/report', methods=['POST'])
def report():
    ID = request.form['ID']
    post_id = request.form['post_id']
    no = cb.report(post_id)
    page = int(request.form['page'])

    return redirect(url_for('read'), code = 307)




@app.route('/revise', methods=['POST'])
def revise():
    ID = request.form['ID']
    post_id = request.form['post_id']
    page = int(request.form['page'])
    post = cb.read(post_id)

    return render_template('revise.html', ID = ID, reading = post, page = page, post_id = post_id)




@app.route('/revising', methods=['POST'])
def revising():
    ID = request.form['ID']
    post_id = request.form['post_id']
    page = int(request.form['page'])
    title = request.form['title']
    content = request.form['content']
    hashtags = request.form['hashtags']
    
    no = cb.revise(post_id, title, content, hashtags)


    return redirect(url_for('read'), code = 307)




@app.route('/delete', methods=['POST'])
def delete():
    ID = request.form['ID']
    post_id = request.form['post_id']
    page = int(request.form['page'])
    cb.delete(post_id)

    return redirect(url_for('community', page = page), code = 307)




########### 댓글 관련 ###########

@app.route('/reply', methods=['POST'])
def reply():
    ID = request.form['ID']
    content = request.form['content']
    post_id = request.form['post_id']
    no = cb.reply(post_id, ID, content)
    page = int(request.form['page'])


    return redirect(url_for('read'), code = 307)




@app.route('/reply_report', methods=['POST'])
def reply_report():
    ID = request.form['ID']
    reply_id = request.form['reply_id']
    
    no = cb.reply_report(reply_id)
    page = int(request.form['page'])


    return redirect(url_for('read'), code = 307)




@app.route('/reply_revise', methods=['POST'])
def reply_revise():
    ID = request.form['ID']
    reply_id = request.form['reply_id']
    content = request.form['content']
    page = int(request.form['page'])

    no = cb.reply_revise(reply_id, content)


    return redirect(url_for('read'), code = 307)




@app.route('/reply_delete', methods=['POST'])
def reply_delete():
    ID = request.form['ID']
    reply_id = request.form['reply_id']

    no = cb.reply_delete(reply_id)
    page = int(request.form['page'])


    return redirect(url_for('read'), code = 307)




########### 검색 ###########

@app.route('/search', methods=['GET'])
def search():
    ID = request.args.get('ID')
    condition = request.args.get('condition')
    
    docs = cb.search(condition)
    if docs == -1:
        docs = {}


    return render_template('community.html', posts = docs, page = 0, ID = ID)




if __name__ == '__main__':
    app.run()