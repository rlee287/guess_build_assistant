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
    gm.onecmd("len 5")
    gm.onecmd("1 w")
    gm.onecmd("2 a")
    gm.onecmd("showclue")
    outstr=outcmd.getvalue()
    assert "wa***"==outstr.rstrip("\n")
    gm.onecmd("list")
    outstr=outcmd.getvalue()
    assert "wagon" in outstr
    assert "fire" not in outstr

