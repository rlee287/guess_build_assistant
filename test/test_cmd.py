from guess_build_assistant.guess_cmd import GuessCmd

import io

# The following tests use the actual wordlist on purpose
def test_help():
    outcmd=io.StringIO()
    gm=GuessCmd("wordlist.txt")
    gm.stdout=outcmd
    gm.onecmd("help")
    # Writing to outcmd advanced the pointer, so use method ignoring that
    outstr=outcmd.getvalue()
    assert gm.doc_header in outstr
    assert not gm.undoc_header in outstr

def test_clue_setup():
    outcmd=io.StringIO()
    gm=GuessCmd("wordlist.txt")
    gm.stdout=outcmd
    gm.AUTOSHOW=False
    gm.onecmd("len 5")
    gm.onecmd("1 b")
    gm.onecmd("clue 3 r")
    gm.onecmd("showclue")
    outstr=outcmd.getvalue()
    assert "b*r**"==outstr.rstrip("\n")

def test_matching():
    outcmd=io.StringIO()
    gm=GuessCmd("wordlist.txt")
    gm.stdout=outcmd
    gm.AUTOSHOW=False
    gm.onecmd("5")
    gm.onecmd("1 w")
    gm.onecmd("hint 2 a")
    gm.onecmd("showclue")
    outstr=outcmd.getvalue()
    assert "wa***"==outstr.rstrip("\n")
    gm.onecmd("list")
    outstr=outcmd.getvalue()
    assert "wagon" in outstr
    assert "fire" not in outstr

def test_badlen():
    outcmd=io.StringIO()
    gm=GuessCmd("wordlist.txt")
    gm.stdout=outcmd
    gm.onecmd("len -56")
    outstr=outcmd.getvalue()
    assert "Error:" in outstr

def test_default_invalid_two():
    outcmd=io.StringIO()
    gm=GuessCmd("wordlist.txt")
    gm.stdout=outcmd
    gm.onecmd("garbase toijgsdf")
    outstr=outcmd.getvalue()
    assert "*** Unknown syntax:" in outstr

def test_default_invalid_numspaces():
    outcmd=io.StringIO()
    gm=GuessCmd("wordlist.txt")
    gm.stdout=outcmd
    gm.onecmd("garbase toi jgs df")
    outstr=outcmd.getvalue()
    assert "*** Unknown syntax:" in outstr

