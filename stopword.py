import re

class Stopword:

    def __init__(self, array):
        self.stopword = array.copy()

    def set_stopword(self, clump):
        clump = clump.casefold();
        clump = re.sub('(\n\r)|[\n\r]', ' ', clump)
        clump = re.sub('(^\s+|\s+$)(.*)', r'\2', clump)
        clump = clump.split()
        self.stopword = clump.copy()

    def get_stopword_raw(self):
        return self.stopword

    def get_stopwod_stringed(self):
        sstopwords = self.stopword.copy()
        sstopwords = '\\b)|(\\b'.join(sstopwords)
        sstopwords = '((\\b' + sstopwords + '\\b))\s?'
        return sstopwords

stopword = Stopword([])