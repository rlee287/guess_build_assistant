from .filter_words import *

import array

class GuessManager(object):
    def __init__(self, wordfile):
        self.wordlist=gen_wordlist(wordfile)
        self.length=0
        # Use array of chars instead of string for subscriptability
        self.clue=array.array('b')

    def set_length(self,length):
        self.length=length
        # Reset clue upon length change
        self.clue=array.array('b',b"*"*length)

    def set_clue(self,pos,char):
        self.clue[pos]=ord(char)

    def get_filtered_list(self):
        return filter_wordlist(self.wordlist, self.clue)
