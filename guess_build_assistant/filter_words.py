from .hashable_lru import hashable_lru

import functools
def gen_wordlist(wordfile):
    """Generates a list of words given a wordfile delimited by whitespace"""
    # read text in
    with open(wordfile,"r") as fil:
        text=fil.read()
    # text.split splits the text into a list based on whitespace
    return text.split()

# Cache repeated calls for checking the same word and pattern
@hashable_lru
def filter_word(word, wordpattern):
    """Checks if a word fits the wordpattern"""
    if len(word)!=len(wordpattern):
        return False
    # Enumerate allows iteration over 
    for ind,char in enumerate(wordpattern):
        if char not in ["*",word[ind]]:
            return False
    return True


# If user undoes a hint, use cache to pull out previous iteration
# Smaller cache as few calls will be made before reset
@hashable_lru
def filter_wordlist(wordlist, wordpattern):
    """Checks a word pattern against the wordlist"""
    return [word for word in wordlist if filter_word(word,wordpattern)]
