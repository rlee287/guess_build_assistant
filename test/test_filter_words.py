import os, sys

import array

import pytest
sys.path.append("..")

from guess_build_assistant.filter_words import *

wordlist_temp_file="ldsreoirkjfd.txt"

@pytest.fixture(scope='function')
def fixture_wordlist(request):
    """Fixture to create and remove a wordlist file"""
    with open(wordlist_temp_file,"w") as fil:
        fil.write("qwertyuiop\nqasdfg hjkl\nzxcvbnm")
    def teardown():
        os.remove(wordlist_temp_file)
    request.addfinalizer(teardown)

def test_wordlist_parse(fixture_wordlist):
    list_words=gen_wordlist(wordlist_temp_file)
    assert len(list_words)==3
    assert list_words[0]=="qwertyuiop"
    assert list_words[1]=="qasdfg hjkl"
    assert list_words[2]=="zxcvbnm"

def test_wordfilter():
    assert filter_word("hihihi","******")
    assert filter_word("hihihi","hi**hi")
    assert filter_word("abcd efg","****-***")
    assert filter_word("abcd efg","**** ***")
    assert not filter_word("qwegfbv","****")
    assert not filter_word("qwfc","qb**")
    assert not filter_word("xy z","*-**")

def test_wordfilter_array():
    array_char=array.array('b',b"**q**")
    assert filter_word("bhq2r",array_char)

def test_listfilter():
    fil_list=filter_wordlist(["pweiq","worheiorhe","ririr"],"***i*")
    assert len(fil_list)==2
    assert fil_list[0]=="pweiq"
    assert fil_list[1]=="ririr"
