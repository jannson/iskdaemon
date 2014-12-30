# -*- coding: UTF-8 -*-
import sys, os
import re
from random import randint
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.fields import Schema, ID, TEXT, NUMERIC
from whoosh.analysis import Tokenizer, Token 
from whoosh import query
from whoosh.query import Every

def group_words(s):
    regex = []

    # Match a whole word:
    regex += [ur'\w+']

    # Match a single CJK character:
    regex += [ur'[\u4e00-\ufaff]']

    # Match one of anything else, except for spaces:
    regex += [ur'[^\s]']

    regex = "|".join(regex)
    r = re.compile(regex)

    return r.findall(s)

class ChineseTokenizer(Tokenizer):
    def __call__(self, text, **kargs):
        token  = Token()
        start_pos = 0
        for w in group_words(text):
            token.original = token.text = w
            token.pos = start_pos
            token.startchar = start_pos
            token.endchar = start_pos + len(w)
            start_pos = token.endchar
            yield token

class SimpleDB(object):
    analyzer = ChineseTokenizer()
    schema = Schema(md5=ID(stored=True), img=NUMERIC(stored=True), content=TEXT(stored=True, analyzer=analyzer))

    def __init__(self, path, is_open=False):
        self.path = path
        if is_open:
            self.ix = create_in(path, self.schema)
        else:
            self.ix = open_dir(path)

    def save(self, md5, img, path):
        writer = self.ix.writer()
        writer.add_document(md5=md5, img=img, content=path)
        writer.commit()
    
    def random(self, size):
        searcher = self.ix.searcher()
        total = searcher.doc_count()
        page_max = total/size
        page = 1
        if page_max > 2:
            page = randint(1, page_max)
        return searcher.search_page(Every("content"), page, size)

    def search(self, q):
        searcher = self.ix.searcher()
        parser = QueryParser("content", schema=self.ix.schema)
        raw_results = searcher.search(parser.parse(q))

    def get(self, md5):
        searcher = self.ix.searcher()
        return searcher.document(md5=md5)

    def get_by_img(self, img):
        searcher = self.ix.searcher()
        return searcher.document(img=img)

simdb_path = "../simdb"
if not os.path.exists(simdb_path):
    os.mkdir(simdb_path)
simpledb = SimpleDB(simdb_path, True)
#simpledb.save(u'aaa1', 2, u'水果世博园')
#print simpledb.get_by_img(2)

'''
for keyword in (u"水果世博园",u"你",u"first",u"中文",u"交换机",u"交换"):
    print "result of ",keyword
    q = parser.parse(keyword)
    results = searcher.search(q)
    for hit in results:  
        print hit.highlights("content")
    print "="*10
'''

