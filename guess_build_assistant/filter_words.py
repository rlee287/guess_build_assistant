from .hashable_lru import hashable_lru

import functools

def gen_wordlist(wordfile):
    """Generates a list of words given a line-delimited wordfile."""
    # read text in
    with open(wordfile,"r") as fil:
        text=fil.read()
    # Split on lines but not spaces because of multiword phrases
    return text.split("\n")

# Cache repeated calls for checking the same word and pattern
#@hashable_lru
def filter_word(word, wordpattern):
    """Checks if a word fits the wordpattern.
       Special character mapping is performed as follows:
       "-" -> " "
       "*" -> <wildcard>"""
    if len(word)!=len(wordpattern):
        return False
    # Enumerate allows iteration over 
    for ind,char in enumerate(wordpattern):
        # Perform type checking to support string and char array wordpattern
        if isinstance(char,str):
            char_comp_pat=char
        else:
            char_comp_pat=chr(char)
        # Handle special chars in wordpattern
        char_comp_word=word[ind]
        if char_comp_pat=="-":
            char_comp_pat=" "
        if char_comp_pat!="*":
            if char_comp_pat!=char_comp_word:
                return False
    return True


# If user undoes a hint, use cache to pull out previous iteration
# Smaller cache as few calls will be made before reset
#@hashable_lru
def filter_wordlist(wordlist, wordpattern):
    """Checks a word pattern against the wordlist."""
    return [word for word in wordlist if filter_word(word,wordpattern)]
