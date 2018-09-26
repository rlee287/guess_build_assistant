import os, sys

#import array

import pytest

sys.path.append("..")

from guess_build_assistant.guess_manager import GuessManager

wordlist_temp_file="ldsreoirkjfd.txt"

@pytest.fixture(scope='module')
def fixture_wordlist(request):
    """Fixture to create and remove a wordlist file"""
    with open(wordlist_temp_file,"w") as fil:
        fil.write("qwertyuiop\nqasdfg jkl\nzxcvbnm")
    def teardown():
        os.remove(wordlist_temp_file)
    request.addfinalizer(teardown)

def test_invalid_wordlist():
    with pytest.raises(FileNotFoundError):
        gm=GuessManager("esroivhdf jhgidsgirdmhdf")

def test_guess_length(fixture_wordlist):
    gm=GuessManager(wordlist_temp_file)
    gm.set_length(7)
    assert gm.length==7
    assert gm.get_cluestr()=="*******"

def test_invalid_length(fixture_wordlist):
    gm=GuessManager(wordlist_temp_file)
    with pytest.raises(ValueError):
        gm.set_length(-5)

def test_guess_match_length(fixture_wordlist):
    gm=GuessManager(wordlist_temp_file)
    gm.set_length(10)
    gm_list_1=gm.get_filtered_list()
    assert len(gm_list_1)==2
    assert "qwertyuiop" in gm_list_1
    assert "qasdfg jkl" in gm_list_1
    assert "zxcvbnm" not in gm_list_1

def test_guess_clue_char(fixture_wordlist):
    gm=GuessManager(wordlist_temp_file)
    gm.set_length(10)
    gm.set_clue(1,"t")
    assert gm.get_cluestr()=="*t********"

def test_guess_clue_override(fixture_wordlist):
    gm=GuessManager(wordlist_temp_file)
    gm.set_length(10)
    gm.set_clue(1,"b")
    assert gm.get_cluestr()=="*b********"
    gm.set_clue(1,"e")
    assert gm.get_cluestr()=="*e********"

def test_invalid_clues(fixture_wordlist):
    gm=GuessManager(wordlist_temp_file)
    gm.set_length(3)
    with pytest.raises(ValueError):
        gm.set_clue(-1,"b")
    with pytest.raises(ValueError):
        gm.set_clue(6,"q")
    with pytest.raises(ValueError):
        gm.set_clue(2,"rhtg")

def test_guess_match_char(fixture_wordlist):
    gm=GuessManager(wordlist_temp_file)
    gm.set_length(7)
    gm.set_clue(0,"z")
    gm_list_2=gm.get_filtered_list()
    assert len(gm_list_2)==1
    assert "qwertyuiop" not in gm_list_2
    assert "qasdfg jkl" not in gm_list_2
    assert "zxcvbnm" in gm_list_2
    gm.set_clue(2,"c")
    gm_list_3=gm.get_filtered_list()
    assert "zxcvbnm" in gm_list_3
