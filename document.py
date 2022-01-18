from sys import argv
from re import match

from stopword import stopword
from errors import *
from tf_idf import TfIdf


class Document:
    def __init__(self, document_name, tf_idf):
        self.document_name = document_name
        self.tf_idf = tf_idf

docs = []

def read_input():
    if len(argv) < 2:
        error(ERRDOCPAR)
    OPTION = ''
    for i in range(1, len(argv)):
        if check_argv(argv, '--help'):
            print('#HELp')
            exit()
        elif not check_argv(argv, '--document'):
            print('#HELp')
            exit()
        elif not check_argv(argv, '--stopword'):
            print('#HELp')
            exit()

        if argv[i] == '--document':
            OPTION = 'DOCUMENT'
        elif argv[i] == '--stopword':
            OPTION = 'STOPWORD'
        elif argv[i]: 
            if (match('.*\.txt$', argv[i])):
                switch(OPTION, argv[i])
            else:
                error(ERRDOCTYPE)
        else:
            print('#HELp')
            exit()

def check_argv(argv, text):
    test = False
    for i, iv in enumerate(argv):
        if iv == text:
            test = True
    return test

def switch(option, filename):
    if option == 'DOCUMENT':
        read_documents(filename)
    elif option == 'STOPWORD':
        read_stopword(filename)
    else:
        error(ERRGENERAL)

def read_documents(filename):
    try:
        file_handler = open(filename, 'rt')
    except FileNotFoundError:
        error(ERRDOCFILE)
    except:
        error(ERRGENERAL)
    tfidf = TfIdf(translate_text(file_handler))
    doc = Document(filename, tfidf)
    docs.append(doc)
    file_handler.close();

def read_stopword(filename):
    try:
        file_handler = open(filename, 'rt')
    except FileNotFoundError:
        error(ERRDOCFILE)
    except:
        error(ERRGENERAL)
    clump = translate_text(file_handler)
    stopword.set_stopword(clump)
    file_handler.close()

def translate_text(file_handler):
    text = ''
    while(1):
        line = file_handler.readline()
        if not line:
            break
        text += line
    return text

def build_tf_idf():
    for i in range(len(docs)):
        docs[i].tf_idf.process()
    for i in range(len(docs)):
        doc_check = []
        for l in range(len(docs)):
            if not i == l:
                per_doc = docs[l].tf_idf.check_doc_unique(docs[i].tf_idf.unique)
                doc_check.append(per_doc)
                kamus_per_doc = {} 
                docs[i].tf_idf.set_dokumen_term_perdoc(per_doc, 'DOC%d' % l)
            else:
                continue
        kamus_final = {}
        for k, kv in enumerate(doc_check):
            for j in kv:
                kamus_final[j] = 0
        for k, kv in enumerate(doc_check):
            for j in kv:
                kamus_final[j] += kv[j]
        docs[i].tf_idf.set_dokumen_term(kamus_final)
    for i in range(len(docs)):
        docs[i].tf_idf.set_idf_value()
        docs[i].tf_idf.set_tf_idf_value()
    
def doc_init():
    read_input()
    build_tf_idf()
