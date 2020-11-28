import ESGuide as es
import re
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime




POST_NUM = "{:>04d}".format(0) #id로 사용
READING_SIZE = 3 #한 페이지에 읽을 게시글 수, 기본값 3




### 껐다 켜도 POST_NUM 유지하도록 글번호 DB에서 관리 ###

def get_pn():
    global POST_NUM

    doc = es.get_doc('post_num', 'post_num')
    if doc == -1:
        POST_NUM = "{:>04d}".format(0)
    else:
        POST_NUM = doc['_source']['POST_NUM']

    return POST_NUM




def update_pn():
    es.insert_doc('post_num', 'post_num', {'POST_NUM' : POST_NUM})




def set_reading_size(reading_size): #READING_SIZE 세팅
    global READING_SIZE
    READING_SIZE = reading_size




def get_datetime(): #현재시간 YYYYMMDDHHMM 형식 반환
    t = datetime.now()
    time = "{:>04d}-{:>02d}-{:>02d}/{:>02d}:{:>02d}".format(t.year, t.month, t.day, t.hour, t.minute)
    return time




def show(category, f): #게시판 리턴 f=from
    if f < 0:
        f += READING_SIZE

    ctgry = es.get_doc('category', category)
    post_ids_ = ctgry['_source']['detail']

    post_ids = None
    for post_ids in post_ids_:
        if post_ids['name'] == 'None':
            break
    post_ids = post_ids['post']
    if len(post_ids) == 0:
        f -= READING_SIZE
        return [{}, f]
    
    match = []
    for _id in post_ids:
        match.append({'match' : {'id':_id}})
    body = {
        'from':f,
        'size':READING_SIZE,
        'sort':{'_id':'desc'},
        'query':{
            'bool':{
                'should':match
                }
            }
        }
    docs = es.search_doc2('post', body)
    

    return [docs, f]


def next_page(f):
    f += READING_SIZE
    
    return f


def back_page(f):
    f -= READING_SIZE

    return f




def read(id): #id를 받아 해당 id의 글을 읽음
    try:
        doc = es.get_doc('post', id)
        replys = es.search_dbr_sorted('reply', 'id', id+"000", id+"1000", [{'_id':'desc'}])

    except:
        return -1

    post = {
        'id' : doc['_id'],
        'ID' : doc['_source']['ID'],
        'title' : doc['_source']['title'],
        'content' : doc['_source']['content'],
        'time' : doc['_source']['time'],
        'recommend' : doc['_source']['recommend'],
        'report' : doc['_source']['report'],
        'hash' : doc['_source']['hash'],
        'replys' : replys
    }


    return post




def post(ID, title, content, hashs, category):
    time = get_datetime()

    #hashs = re.sub(' ', '', hashs)
    #hashtags = hashs.split('#')
    #hastags = hashs.remove('')
    
    global POST_NUM
    get_pn()

    post = {
        'id' : POST_NUM,
        'ID' : ID,
        'title' : title,
        'content' : content,
        'time' :time,
        'recommend' : 0,
        'report' : 0,
        'hash' : hashs
    }
    r = es.addToCategory(category, 'None', 'post', POST_NUM)
    if r == -1:
        print('error!')
        return -1

    es.insert_doc('post', POST_NUM, post)
    pn = int(POST_NUM) + 1
    if(pn > 9999):
        return -1
    POST_NUM = "{:>04d}".format(pn)
    update_pn()


    return POST_NUM




def revise(id, title, content, hashs, originalC, category):
    doc = es.get_doc('post', id)
    doc['_source']['title'] = title
    doc['_source']['content'] = content
    time = get_datetime()
    doc['_source']['time'] = time
    doc['_source']['hash'] = hashs
    
    es.deleteFromCategory(originalC, 'None', 'post', doc['_id'])
    es.addToCategory(category, 'None', 'post', doc['_id'])
    es.insert_doc('post', doc['_id'], doc['_source'])


    return doc['_id']




def delete(id, category):
    es.delete_doc('post', id)
    es.deleteFromCategory(category, 'None', 'post', id)

    return id




def recommend(id):
    doc = es.get_doc('post', id)
    doc['_source']['recommend'] += 1
    es.insert_doc('post', doc['_id'], doc['_source'])


    return doc['_id']




def report(id):
    doc = es.get_doc('post', id)
    doc['_source']['report'] += 1
    es.insert_doc('post', doc['_id'], doc['_source'])


    return doc['_id']




def reply(id, ID, content):
    replys = es.search_dbr_sorted('reply', 'id', id+"000", id+"1000", [{'_id':'desc'}])

    time = get_datetime()
    reply = {
        'ID' : ID,
        'content' : content,
        'time' : time,
        'report' : 0
    }

    if replys == -1:
        reply['id'] = id + "000"
        n = es.insert_doc('reply', id+"000", reply)

    else:
        _len = len(replys)
        reply_id = "{:>03d}".format(_len)
        reply['id'] = id + reply_id
        n = es.insert_doc('reply', id+reply_id, reply)


    return id




def reply_report(reply_id):
    reply = es.get_doc('reply', reply_id)

    reply['_source']['report'] += 1
    es.insert_doc('reply', reply['_id'], reply['_source'])


    return reply_id[0:4]




def reply_revise(reply_id, content):
    reply = es.get_doc('reply', reply_id)
    reply['_source']['content'] = content
    es.insert_doc('reply', reply_id, reply['_source'])


    return reply_id[0:4]




def reply_delete(reply_id):
    es.delete_doc('reply', reply_id)

    return reply_id[0:4]




def search(condition):
    body = {
        'sort':{'_id':'desc'},
        'query':{
            'bool':{
                'should':[
                    {
                    'match':{
                        'title':condition
                    }
                    },
                    {
                    'match':{
                        'hash':condition
                    }
                    }
                ]
            }
        }
    }
    docs = es.search_doc2('post', body)


    return docs