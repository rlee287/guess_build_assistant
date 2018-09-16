from .filter_words import *

import array

class GuessManager(object):
    def __init__(self, wordfile):
        self.wordlist=gen_wordlist(wordfile)
        self.length=0
        # Use array of chars instead of string for subscriptability
        self.clue=array.array('b')

    def set_length(self,length):
        if length<=0:
            raise ValueError("Length must be positive")
        self.length=length
        # Reset clue upon length change
        self.clue=array.array('b',b"*"*length)

    def set_clue(self,pos,char):
        if pos<0 or pos>=self.length:
            raise ValueError("Position must be within clue")
        try:
            self.clue[pos]=ord(char)
        except TypeError:
            # Want this to be ValueError
            raise ValueError("Second argument must be a single character")

    def get_cluestr(self):
        # Assuming only ascii for now
        return self.clue.tobytes().decode("utf-8")

    def get_filtered_list(self):
        return filter_wordlist(self.wordlist, self.clue)
