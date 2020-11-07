# ElasticSearch Guide

# 만드시는 py 파일과 같은 폴더에 넣어두고
# import ESGuide as es 하신 후
# es.insert_idx() 처럼 사용하시면 됩니다!

# 함수의 return 값 중 여러개가 반환될 만한 것들은 리스트로 반환됩니다
# for doc in (return받은 값): 처럼 사용하셔서 각 doc에 접근하실 수 있고
# 각 doc에서는 doc['_id']로 pid에 doc['_source']로 필드에 접근할 수 있습니다!

from elasticsearch import Elasticsearch
from elasticsearch import helpers

es = Elasticsearch('localhost:9200', timeout=30)
es.indices.delete(index='*') #테스트 끝나면 삭제

#필요한 테이블들 생성
#테이블 이름은 모두 소문자로 작성해주세요
#테이블 추가, 이름 수정 가능
idxs = ['account', 'teacher', 'class', 'category', 'regist_request', 'post', 'reply']
for idx in idxs:
        if not es.indices.exists(index=idx):
                es.indices.create(index=idx)


#index 가져오기
def get_idx(idx):
        if es.indices.exists(index=idx):
                data = es.search(index=idx, body={'query':{'match_all':{}}})
                return data['hits']['hits']
        else:
                print("Error: idx does not exist.")
                return -1


#document 저장
def insert_doc(idx, pid, doc):
        try:
                es.index(index=idx, id=pid, body=doc)
        except:
                print("Error: doc's data format is different from idx's data format")
                return -1

        es.indices.refresh(index=idx)
        return 0


#document 여러개 저장
def insert_docs(idx, pids, docs): #idx에 pids[0]로 docs[0]를 ... pids[n]으로 docs[n]을 넣겠다
        if len(pids)!=len(docs):
                print("Error: pids's & docs's length must be same.")
                return -1
        
        _docs = []
        for pid, doc in zip(pids, docs):
                _docs.append({
                        '_index' : idx,
                        '_id' : pid,
                        '_source' : doc
                        })
        helpers.bulk(es, _docs)

        es.indices.refresh(index=idx)
        return 0


#pid로 document 가져오기
def get_doc(idx, pid):
        try:
                doc = es.get(index=idx, id=pid)
                return doc
        except:
                print("Error: data does not exist.")
                return -1


#pids에 해당하는 documents 가져오기
def get_docs(idx, pids): #idx의 pid=pids[0], pids[1] ... pids[n]인 데이터들을 가져옴
        try:
                ids = {'ids' : pids}
                docs = es.mget(index=idx, body=ids)
                return docs['docs']
        except:
                print("Error: data does not exist.")
                return -1


#조건으로 document 찾기
def search_doc(idx, cond): #cond는 tuple 형태
        try:
                condition = {'query':{'match':cond}}
                res = es.search(index=idx, body=condition)
                return res['hits']['hits']
        except:
                print("Error: data does not exist.")
                return -1


#pid로 doc 지우기
def delete_doc(idx, pid):
        try:
                es.delete(index=idx, id=pid)
        except:
                return -1
        
        es.indices.refresh(index=idx)
        return 0


#테이블별 데이터 형식
#pid는 모두 String 형태로 통일해주세요!
#★데이터 형식이 반드시 같아야 doc 저장이 됩니다★
if __name__=='__main__':
        account = { #pid = ID
                'PW' : 'String',
                'name' : 'String',
                'age' : int(0), #만나이로 통일
                'birth' : 'String', #YYYYMMDD
                'phone' : 'String', #'-'포함
                'T' : False #Teacher, Teacher > True, Student > False
                }
        insert_doc('account', 'guide', account)

        teacher = { #pid = ID
                'certificate_num' : int(0),
                'place' : 'String' #OOO도 OO시 / OOOO시
                }
        insert_doc('teacher', 'guide', teacher)

        _class = { #pid = class_num
                'ID' : 'String',
                'c_name' : 'String',
                'cost' : int(0),
                'when' : 'String', #YYYYMMDDHHMM (시간은 24시간 단위)
                'M' : False, #Meet, Offline > True, Online > False
                }
        insert_doc('class', 'guide', _class)

        category = { #pid = 00, 01 ...
                'name' : 'String', #huge category name
                'detail' : [] #detail category names
                }
        insert_doc('category', 'guide', category)

        regist_request = { #pid = regist_num
                'class' : 'String', #class_num
                'ID' : 'String'
                }
        insert_doc('regist_request', 'guide', regist_request)
        
        post = { #pid = post_num
                'ID' : 'String',
                'title' : 'String',
                'content' : 'String',
                'time' : 'String', #YYYYMMDDHHMM (시간은 24시간 단위)
                'recommend' : int(0),
                'report' : int(0)
                }
        insert_doc('post', 'guide', post)

        reply = { #pid = post_num
                'ID' : 'String',
                'content' : 'String',
                'time' : 'String', #YYYYMMDDHHMM (시간은 24시간 단위)
                'report' : int(0)
                }
        insert_doc('reply', 'guide', reply)

