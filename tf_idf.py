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

    def get_text_output(self, no_kalimat):
        output_text = sub('\s+', ' ', self.kalimat)
        output_text = sub('(\.)', '.|?', output_text)
        output_text = output_text.split('|?')
        kamus = {}
        for l, lv in enumerate(output_text):
            Sn = 'S%d' % l
            kamus[Sn] = lv
        text = ''
        for i, iv in enumerate(no_kalimat):
            text += kamus[iv['data']]
        # print(kamus)
        text = sub('(^\s+|\s+$)(.*)', r'\2', text)
        return text     

    # Melakukan pengecekan array kata unique pada it_idf ini
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
        kalimat_len = len(self.stopword_val) # 8
        for i in self.frekuensi_term:
            if self.frekuensi_term[i] == 0:
                SnDf = 0
            else:
                SnDF = round(kalimat_len/self.frekuensi_term[i], 3)
            self.idf_val[i] = log(SnDF, 10)

    def set_tf_idf_value(self):
        tf_idf = {}
        total_tf_idf = {}
        # Inisialisasi 0
        for l in range(len(self.stopword_val)):
            Sn = 'S%d' % l # S0 S1 S2 S3
            total_tf_idf[Sn] = 0 # S1 = 0 S2 = 0
        # Proses pencarian
        S2 = 0
        S3 = 0
        for l in self.frekuensi_term_perkalimat: # l = 'rencana'
            sub = {}
            for i in range(len(self.stopword_val)): # i = 0
                Sn = 'S%d' % i # S0 
                # Sub = {'S0': idf_val['rencana'] * frekuensi_term_perkalimat['rencana']['S0'], 'S1'...}
                sub[Sn] = self.idf_val[l] * self.frekuensi_term_perkalimat[l][Sn] 
                total_tf_idf[Sn] = total_tf_idf[Sn] + sub[Sn]
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
        # add_split = sub('(\.\s)', '.|?', one_liner)
        kalimat_pecahan = one_liner.split('.')
        for index, line in enumerate(kalimat_pecahan):
            self.perkalimat.append(line)

    def filtering(self):
        for index, line in enumerate(self.perkalimat):
            filter_kalimat = sub('[\!\(\<\]\@\)\:\|\#\.\;\\\$\,\/\+\%\„\?\=\^\"\{\_\&\}\,\*\>\[\t\r\n(\(.*\))]|(\d+\/\d+\/\d+)', '', line)
            filter_kalimat = sub('[\-|\s{2,}]', ' ', filter_kalimat)
            filter_kalimat = sub('(^\s+|\s+$)(.*)', r'\2', filter_kalimat)
            if filter_kalimat:
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
        # unique = ['rencana', 'jakarta']
        for i, iv in enumerate(self.unique):
            nums = [] # S0: 1, S2: 2, S3: 0, ..., S7: 0
            total = 0
            for l, lv in enumerate(self.stopword_val):
                num = 0
                regex = '\\b%s\\b' % iv
                appear = findall(regex, lv) # return ['rencana', 'rencana']
                num = len(appear) # 2
                total += num
                nums.append(num)
            kamus = {}
            # kamus = {'asd': kv}
            for k, kv in enumerate(nums):
                kamus['S%d' % k] = kv
            self.frekuensi_term_perkalimat[iv] = kamus
            self.frekuensi_term[iv] = total

    def set_dokumen_term(self, dokumen_term):
        self.dokumen_term = dokumen_term.copy()
 
    def set_dokumen_term_perdoc(self, dokumen_term, doc_name):
        self.dokumen_term_perdoc[doc_name] = dokumen_term


