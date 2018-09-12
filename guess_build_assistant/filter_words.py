import functools

"""
Generates a list of words given a wordfile delimited by whitespace
"""
def gen_wordlist(wordfile):
    # read text in
    with open(wordfile,"r") as fil:
        text=fil.read()
    # text.split splits the text into a list based on whitespace
    return text.split()

"""
Checks if a word fits the wordpattern
"""
# Cache repeated calls for checking the same word and pattern
@functools.lru_cache(1024)
def filter_word(word, wordpattern):
    if len(word)!=len(wordpattern):
        return False
    # Enumerate allows iteration over 
    for ind,char in enumerate(wordpattern):
        if wordpattern[ind] not in ["*",word[ind]]:
            return False
    return True


# If user undoes a hint, use cache to pull out previous iteration
# Smaller cache as few calls will be made before reset
@functools.lru_cache(maxsize=16)
def filter_wordlist(wordlist, wordpattern):
    return [word for word in wordlist if filter_word(word,wordpattern)]
