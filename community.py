import community_base as cb
from flask import Blueprint, render_template, request, redirect, url_for, session
import string
import random




bp_community = Blueprint('community', __name__)

CATEGORIES = ['art', 'beauty', 'cooking', 'experience']




########### 로그인 ###########

# @bp_community.route('/')
# def main():
#     return render_template('login.html')


# @bp_community.route('/login', methods=['POST'])
# def login():
#     ID = request.form['ID']
#     session['user_id'] = ID

#     return redirect(url_for('community.community', page = 0))




########### 페이지 관련 ###########

@bp_community.route('/community', methods=['GET'])
def community():
    ID = session.get('user_id')
    category = request.args.get('category')
    page = int(request.args.get('page'))

    htmlname = 'main_community.html'
    docs = {}
    hots = {}
    if category != None:
        docs, hots, page = cb.show(category, page)
        htmlname = 'community_' + category + '.html'

    return render_template(htmlname, categories = CATEGORIES, hots = hots, posts = docs, ID = ID, category = category, page = page)


@bp_community.route('/nextpage', methods=['POST'])
def nextpage():
    category = request.form['category']
    page = int(request.form['page'])
    page = cb.next_page(page)

    return redirect(url_for('community.community', category = category, page = page))


@bp_community.route('/backpage', methods=['POST'])
def backpage():
    category = request.form['category']
    page = int(request.form['page'])
    page = cb.back_page(page)

    return redirect(url_for('community.community', category = category, page = page))




########### 글쓰기 ###########

@bp_community.route('/post', methods=['POST'])
def post():
    ID = session.get('user_id')
    category = request.form['category']

    return render_template('post.html', ID = ID, categories = CATEGORIES, category = category)

@bp_community.route('/posting', methods=['POST'])
def posting():
    ID = session.get('user_id')
    title = request.form['title']
    content = request.form['content']
    hashtags = request.form['hashtags']
    category = request.form['category']
    
    cb.post(ID, title, content, hashtags, category)


    return redirect(url_for('community.community', category = category, page = 0))




########### 글읽기 ###########

@bp_community.route('/read', methods=['POST'])
def read():
    ID = session.get('user_id')
    post_id = request.form['post_id']
    page = int(request.form['page'])
    category = request.form['category']
    post = cb.read(post_id)


    return render_template('read.html', reading = post, login = ID, page = page, category = category)
    



@bp_community.route('/recommend', methods=['POST'])
def recommend():
    post_id = request.form['post_id']
    no = cb.recommend(post_id)

    return redirect(url_for('community.read'), code = 307)




@bp_community.route('/report', methods=['POST'])
def report():
    post_id = request.form['post_id']
    no = cb.report(post_id)

    return redirect(url_for('community.read'), code = 307)




@bp_community.route('/revise', methods=['POST'])
def revise():
    ID = session.get('user_id')
    post_id = request.form['post_id']
    page = int(request.form['page'])
    category = request.form['category']
    post = cb.read(post_id)

    return render_template('revise.html', ID = ID, post = post, page = page, post_id = post_id, categories = CATEGORIES, category = category)




@bp_community.route('/revising', methods=['POST'])
def revising():
    post_id = request.form['post_id']
    page = int(request.form['page'])
    title = request.form['title']
    content = request.form['content']
    hashtags = request.form['hashtags']
    originalC = request.form['originalC']
    category = request.form['category']
    
    no = cb.revise(post_id, title, content, hashtags, originalC, category)


    return redirect(url_for('community.read'), code = 307)




@bp_community.route('/delete', methods=['POST'])
def delete():
    post_id = request.form['post_id']
    category = request.form['category']
    page = int(request.form['page'])
    cb.delete(post_id, category)

    return redirect(url_for('community.community', category = category, page = page))




########### 댓글 관련 ###########

@bp_community.route('/reply', methods=['POST'])
def reply():
    ID = session.get('user_id')
    content = request.form['content']
    post_id = request.form['post_id']
    no = cb.reply(post_id, ID, content)
    page = int(request.form['page'])


    return redirect(url_for('community.read'), code = 307)




@bp_community.route('/reply_report', methods=['POST'])
def reply_report():
    reply_id = request.form['reply_id']
    
    no = cb.reply_report(reply_id)
    page = int(request.form['page'])


    return redirect(url_for('community.read'), code = 307)




@bp_community.route('/reply_revise', methods=['POST'])
def reply_revise():
    reply_id = request.form['reply_id']
    content = request.form['content']
    page = int(request.form['page'])

    no = cb.reply_revise(reply_id, content)


    return redirect(url_for('community.read'), code = 307)




@bp_community.route('/reply_delete', methods=['POST'])
def reply_delete():
    reply_id = request.form['reply_id']

    no = cb.reply_delete(reply_id)
    page = int(request.form['page'])


    return redirect(url_for('community.read'), code = 307)




########### 검색 ###########

@bp_community.route('/search', methods=['POST'])
def search():
    ID = session.get('user_id')
    category = request.form['category']
    condition = request.form['search']
    
    docs = cb.search(category, condition)
    if docs == -1:
        docs = {}
    
    htmlname = 'community_' + category + '.html'


    return render_template(htmlname, categories = CATEGORIES, category = category, posts = docs, page = 0, ID = ID)




#if __name__ == '__main__':
    #bp_community.run(host = '127.0.0.1', port = 5000, debug = True)
    #bp_community.run(host = '0.0.0.0')