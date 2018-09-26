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
    gm.onecmd("11")
    gm.onecmd("6 -")
    gm.onecmd("1 g")
    gm.onecmd("list")
    outstr=outcmd.getvalue()
    assert "glass table" in outstr
    assert "orange juice" not in outstr

def test_matching_override():
    outcmd=io.StringIO()
    gm=GuessCmd("wordlist.txt")
    gm.stdout=outcmd
    gm.AUTOSHOW=False
    gm.onecmd("7")
    gm.onecmd("5 i")
    gm.onecmd("hint 7 g")
    gm.onecmd("hint 2 a")
    gm.onecmd("list")
    outstr=outcmd.getvalue()
    assert "raining" in outstr
    assert "snowing" not in outstr
    curpos=outcmd.tell()
    gm.onecmd("clue 2 n")
    gm.onecmd("list")
    outcmd.seek(curpos)
    outstr=outcmd.read()
    assert "snowing" in outstr
    assert "raining" not in outstr

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

