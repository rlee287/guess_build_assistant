from guess_build_assistant.guess_cmd import GuessCmd

import io

def test_help():
    outcmd=io.StringIO()
    gm=GuessCmd("wordlist.txt")
    gm.stdout=outcmd
    var=gm.onecmd("help\n")
    # Writing to outcmd advanced the pointer, so use method ignoring that
    outstr=outcmd.getvalue()
    assert gm.doc_header in outstr
    assert not gm.undoc_header in outstr
