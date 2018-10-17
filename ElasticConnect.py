import logging
from os import listdir
from elasticsearch import Elasticsearch
import json


INDEX_NAME = 'java'
INDEX_TYPE = 'java_programming'
BaseDir = 'Data'
def connect_elasticsearch():
    _es = None
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if _es.ping():
        print('Yay Connect')
    else:
        print('Awww it could not connect!')
    return _es


def create_index(es_object, index_name='Java'):
    exception_filenames = []
    for f in listdir(BaseDir):
        print('Filename :',f)
        try:
            # Ignore 400 means to ignore "Index Already Exist" error.
            with open(BaseDir + '/' + f) as fr:
                data = json.load(fr)
            es_object.index(index=INDEX_NAME, doc_type=INDEX_TYPE, body=data)
            print('Created Index')
        except Exception as ex:
            exception_filenames.append(f)
            print('Exception occured : ',str(ex))
    print(exception_filenames)


def search(es_object):
    try:
        res = es_object.search(index=INDEX_NAME, doc_type=INDEX_TYPE, body={"query": {"match": {"content": "array"}}}, size=10, sort='_score')
        #print(res['hits']['total'])
        #print('Response : ',res)
        for i in range(len(res['hits']['hits'])):
            res_data = res['hits']['hits'][i]
            print('Content : %s with score of %f'%(res_data['_source']['content'], res_data['_score']))
            print('\n')
    except Exception as exp:
        print('Exception in search : ', exp)

if __name__ == '__main__':
  logging.basicConfig(level=logging.ERROR)
  es_obj = connect_elasticsearch()
  #create_index(es_obj)
  search(es_obj)
  # es_obj.indices.delete(index=INDEX_NAME)
  #es_obj.search(index=,doc_type=,body=,)