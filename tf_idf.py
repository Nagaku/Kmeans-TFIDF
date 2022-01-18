from re import findall, sub
from math import log
from stopword import stopword

class TfIdf:
    def __init__(self, kalimat):
        self.kalimat = kalimat
        self.casefold = []
        self.perkalimat = []
        self.filter = []
        self.token = []
        self.stopword_val = []
        self.unique = []
        self.frekuensi_term = {}
        self.frekuensi_term_perkalimat = {}
        self.dokumen_term = {}
        self.dokumen_term_perdoc = {}
        self.idf_val = {}
        self.tf_idf_val = {}

    def check_doc_unique(self, unique):
        dokumen_term = {}
        for i, iv in enumerate(unique):
            nums = 0
            for l, lv in enumerate(self.stopword_val):
                regex = '\\b%s\\b' % iv
                appear = findall(regex, lv)
                num = len(appear)
                nums += num
            dokumen_term[iv] = nums;
        return dokumen_term

    def set_idf_value(self):
        # if len(self.dokumen_term_perdoc) == 0:
        kalimat_len = len(self.stopword_val)
        for i in self.frekuensi_term:
            SnDF = round(kalimat_len/self.frekuensi_term[i], 3)
            self.idf_val[i] = round(log(SnDF, 10), 3)

    def set_tf_idf_value(self):
        tf_idf = {}
        total_tf_idf = {}
        for l in range(len(self.stopword_val)):
            Sn = 'S%d' % l
            total_tf_idf[Sn] = 0
        for l in self.frekuensi_term_perkalimat:
            sub = {}
            for i in range(len(self.stopword_val)):
                Sn = 'S%d' % i
                sub[Sn] = self.idf_val[l] * self.frekuensi_term_perkalimat[l][Sn]
                total_tf_idf[Sn] = round(total_tf_idf[Sn] + sub[Sn], 3)
            tf_idf[l] = sub
        self.tf_idf_val = total_tf_idf

    
    def process(self):
        self.case_folding()
        self.pemecah_kalimat()
        self.filtering()
        self.stopword_removal()
        self.tokenizing()
        self.set_unique()
        self.set_frekuensi_term()

    def case_folding(self):
        self.case_fold = self.kalimat.casefold()

    def pemecah_kalimat(self):
        one_liner = sub('(\r\n)|[\r\n]', ' ', self.case_fold)
        add_split = sub('(\.\s)', '.|?', one_liner)
        kalimat_pecahan = add_split.split('|?')
        for index, line in enumerate(kalimat_pecahan):
            self.perkalimat.append(line);

    def filtering(self):
        for index, line in enumerate(self.perkalimat):
            filter_kalimat = sub('[\!\(\<\]\@\)\:\|\#\.\;\\\$\,\/\+\%\„\?\=\^\"\{\_\&\}\,\*\>\[\t\r\n(\(.*\))]|(\d+\/\d+\/\d+)', '', line)
            filter_kalimat = sub('[\-|\s{2,}]', ' ', filter_kalimat)
            filter_kalimat = sub('(^\s+|\s+$)(.*)', r'\2', filter_kalimat)
            self.filter.append(filter_kalimat)

    def stopword_removal(self):
        stopwords = stopword.get_stopwod_stringed()
        for index, line in enumerate(self.filter):
            remove_stopword = sub(stopwords, '', line)
            self.stopword_val.append(remove_stopword)

    def tokenizing(self):
        for index, line in enumerate(self.stopword_val):
            tokenize = line.split()
            self.token.append(tokenize)

    def set_unique(self):
        self.unique = self.token.copy()
        unique = self.unique[0].copy()
        for i in range(1, len(self.unique)):
            for index, word in enumerate(self.unique[i]):
                if word not in unique:
                    unique.append(word)
        self.unique = unique

    def set_frekuensi_term(self):
        for i, iv in enumerate(self.unique):
            nums = []
            total = 0
            for l, lv in enumerate(self.stopword_val):
                num = 0
                regex = '\\b%s\\b' % iv
                appear = findall(regex, lv)
                num = len(appear)
                total += num
                nums.append(num)
            kamus = {}
            for k, kv in enumerate(nums):
                kamus['S%d' % k] = kv
            self.frekuensi_term_perkalimat[iv] = kamus
            self.frekuensi_term[iv] = total
            

    def set_dokumen_term(self, dokumen_term):
        self.dokumen_term = dokumen_term.copy()
 
    def set_dokumen_term_perdoc(self, dokumen_term, doc_name):
        self.dokumen_term_perdoc[doc_name] = dokumen_term


