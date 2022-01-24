from sys import argv
from re import match
from os.path import exists
from os import mkdir
from stopword import stopword
from errors import *
from tf_idf import TfIdf
from time import gmtime, strftime


class Document:
    def __init__(self, document_name, tf_idf):
        self.document_name = document_name
        self.tf_idf = tf_idf

docs = []
OUTPUT = False

# Menerima input dari terminal dan melakukan pengecekan
def read_input():
    # Tidak ada masukan
    if len(argv) < 2:
        error(ERRDOCPAR)
    # Masukan tidak lengkap
    if check_argv(argv, '--help'):
        print('#HELp')
        exit()
    elif not check_argv(argv, '--document'):
        print('#HELp')
        exit()
    elif not check_argv(argv, '--stopword'):
        print('#HELp')
        exit()


    OPTION = ''
    for i in range(1, len(argv)):

        if argv[i] == '--document':
            OPTION = 'DOCUMENT'
        elif argv[i] == '--stopword':
            OPTION = 'STOPWORD'
        elif argv[i] == '--output':
            OPTION = 'output'
            global OUTPUT
            OUTPUT = True
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

# Mengubah menjadi satu baris
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
    
def write_output(filename, text):
    global OUTPUT
    if OUTPUT:
        if not exists('output'):
            mkdir('output')
        fn = 'output/' + filename + strftime("_%a_%d_%b_%Y_%H_%M_%S.txt", gmtime())
        file_output = open(fn, 'at')
        file_output.write(text)
        file_output.close()
        print('File output di %s' % fn)

# entry document.py
def doc_init():
    read_input()
    build_tf_idf()