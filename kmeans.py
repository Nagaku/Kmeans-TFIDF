from document import docs, doc_init
from random import randint
from errors import *
from sys import maxsize
from copy import deepcopy

jumlah_cluster = 2

kmeans = []

class Cluster:
    def __init__(self, cluster_name, centeroid):
        self.cluster_name = cluster_name
        self.centeroid = centeroid
        self.anggota = []
        self.total = 0

    def calculate_centeroid(self):
        mean = 0
        for l, lv in enumerate(self.anggota):
            # print(lv['data'], lv['value'])
            mean += lv['value']
        if len(self.anggota) == 0:
            self.centeroid = 0
        else:
            self.centeroid = mean/len(self.anggota)

    def get_cluster_stringed(self):
        pre = '%s: %.3f: ' % (self.cluster_name, round(self.centeroid,3))
        for i, iv in enumerate(self.anggota):
            pre += ' ['
            pre += '%s:%.3f:' % (iv['data'], round(iv['value'], 2))
            pre += '{'
            for l in iv['diff']:
                pre += '%s:%.3f,' % (l, round(iv['diff'][l], 2))
            pre += '}'
            pre += '] '
        return pre

    def get_total(self):
        self.total = 0
        for l, lv in enumerate(self.anggota):
            self.total += lv['value']

class Kmeans:
    def __init__(self, document_name, cluster, data):
        self.document_name = document_name
        self.data = data
        self.prev_cluster = cluster
        self.cluster = cluster

    def calculate_all_centeroid(self):
        for l, lv in enumerate(self.cluster):
            lv.calculate_centeroid()
        
    def calculate_diff(self):
        self.prev_cluster = deepcopy(self.cluster)
        for l, lv in enumerate(self.cluster):
            lv.anggota = []
        for i in self.data:
            iv = self.data[i]
            min_val = {'val': maxsize, 'index': 0}
            comparision = {}
            for l, lv in enumerate(self.cluster):
                comparision[lv.cluster_name] = round(abs(lv.centeroid-iv), 3)
                if abs(lv.centeroid-iv) < min_val['val']:
                    min_val = {'val': abs(lv.centeroid-iv), 'index': l}
            self.cluster[min_val['index']].anggota.append({'data': i, 'value': iv, 'diff': comparision})

    def check_changes(self):
        ret = True
        for l, lv in enumerate(self.cluster):
            for i, iv in enumerate(lv.anggota):
                if len(self.prev_cluster[l].anggota) < 1:
                    return True
                if self.prev_cluster[l].anggota[i]['data']:
                    if iv['data'] == self.prev_cluster[l].anggota[i]['data']:
                        ret = False
                    else:
                        return True
        return ret

    def pick_highest(self):
        for l, lv in enumerate(self.cluster):
            return
    
def define_kmeans():
    for i, iv in enumerate(docs):
        if jumlah_cluster > len(iv.tf_idf.stopword_val):
            error(ERRCLUSNUM)
    for i, iv in enumerate(docs):
        doc = []
        used = []
        for i in range(jumlah_cluster):
            random_int = randint(0, len(iv.tf_idf.tf_idf_val)-1)
            while random_int in used:
                random_int = randint(0, len(iv.tf_idf.tf_idf_val)-1)
            used.append(random_int)
            doc.append(Cluster('C%d' % i, iv.tf_idf.tf_idf_val['S%d' % random_int]))
            # doc.append(Cluster('C%d' % i, iv.tf_idf.tf_idf_val['S%d' % i]))
        kmeans.append(Kmeans(iv.document_name, doc, iv.tf_idf.tf_idf_val))

def get_bool(bool_val):
    if bool_val:
        return 'Ya'
    return 'Tidak'

def kmeans_init():
    doc_init()
    define_kmeans()
    
    for i, iv in enumerate(kmeans):
        print(iv.document_name)
        it = 0

        while 1:
            iv.calculate_diff()
            print('\nIterasi %d changed? %s' % (it, get_bool(iv.check_changes())))
            it += 1
            print(iv.cluster[0].get_cluster_stringed())
            print(iv.cluster[1].get_cluster_stringed())
            iv.calculate_all_centeroid()
            if not iv.check_changes():
                break
            
        iv.calculate_diff()
        print('\nIterasi %d changed? %s' % (it, get_bool(iv.check_changes())))
        it += 1
        print(iv.cluster[0].get_cluster_stringed())
        print(iv.cluster[1].get_cluster_stringed())
        iv.calculate_all_centeroid()
        print('\n')



