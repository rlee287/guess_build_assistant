import cmd
from .guess_manager import GuessManager

# Utility func
def _validate_clue_args(args):
    """Returns 0 if OK for hint,
       1 for nonconforming args,
       2 for bad char,
       3 for other bad args,
       8 for only one arg
       Deliberately skips length check as that is performed elsewhere"""
    argslist=args.split()
    if len(argslist)==1:
        return 8
    if len(argslist)!=2:
        return 1
    try:
        int(argslist[0])
    except ValueError:
        return 1
    if len(argslist[1])>1:
        return 1
    if argslist[1] not in "qwertyuiopasdfghjklzxcvbnm-*1234567890":
        return 2
    return 0

class GuessCmd(cmd.Cmd):
    helpstr = """Overview of commands:
       "help" Prints out help information
       "reset" Resets the game to begin anew.
       "len <number>" Sets the length of the word.
       "hint <number> <character>" Sets a hint position.
       "clue <number> <character>" Alias for "hint".
       "<number>" Alias for "len" without a prefix.
       "<number> <character>" Alias for "hint" without a prefix.
       "wordlist <optional path>" Prints the wordlist or
                                  sets the wordlist if path is given.
       "showlist" Shows the filtered list of possible words.
       "show" Alias for "showlist".
       "list" Alias for "showlist".
       "showclue" Shows the clue so far.
       "exit" or "quit" Quits the application.
    """
    intro = "Welcome to Guess Build Assistant!\n"+helpstr
    prompt = "guess>>> "

    def __init__(self, wordlist):
        self.wordlist = wordlist
        self.guess_manager = GuessManager(wordlist)
        super().__init__()

    def emptyline(self):
        # Do nothing
        pass

    def do_reset(self, args):
        """Resets the game to begin anew."""
        # Create new guess manager and cleanup old one
        self.guess_manager = GuessManager(self.wordlist)

    def do_wordlist(self, args):
        """Prints out the wordlist or sets a new one."""
        if args:
            self.wordlist=args
            self.do_reset(None)
        else:
            self.stdout.write("Wordlist is {}\n".format(self.wordlist))

    def do_len(self, args):
        """Sets the length of the word."""
        int_len=0
        try:
            int_len=int(args)
            # Automatically catches negatives
            self.guess_manager.set_length(int_len)
        except ValueError:
            self.stdout.write("Error: {} is not a valid length\n"
                                    .format(repr(args)))

    def default(self, line):
        # Do parsing again here
        errstat=_validate_clue_args(line)
        if errstat==1:
            super().default(line)
            return
        if errstat==8:
            self.do_len(line)
            return
        self.do_hint(line)

    def do_clue(self, args):
        """Sets a clue.
           Inputs are of the format <number> <character>, in which
           <number> is the letter position and <character> is the letter.
           Use "*" for the character to reset a hint.
        """
        self.do_hint(args)

    def do_hint(self, args):
        """Sets a clue.
           Inputs are of the format <number> <character>, in which
           <number> is the letter position and <character> is the letter.
           Use "*" for the character to reset a hint.
        """
        errstat=_validate_clue_args(args)
        argslist=args.split()
        if errstat==1:
            self.stdout.write("Error: args must be of the form <number> <character>\n")
            return
        if errstat==2:
            self.stdout.write("Error: char must be a letter, "+
                              "hyphen (space), digit, or asterisk\n")
            return
        # TODO: Fix DRY violation by finding way to pass out parse results
        int_pos=-1
        try:
            int_pos=int(argslist[0])
        except ValueError:
            self.stdout.write("Error: args must be of the form <number> <character>\n")
            return
        # UI is 1 based, program is 0 based
        try:
            self.guess_manager.set_clue(int_pos-1,argslist[1])
        except ValueError as ve:
            if "Position" in ve.args[0]:
                self.stdout.write("Error: position must be within the clue length\n")
                return
            else:
                raise

    def do_showclue(self, args):
        """Shows the current clue."""
        self.stdout.write(self.guess_manager.get_cluestr())
        self.stdout.write("\n")

    def do_show(self, args):
        """Shows the current filtered list."""
        self.do_showlist(args)

    def do_list(self, args):
        """Shows the current filtered list."""
        self.do_showlist(args)

    def do_showlist(self, args):
        """Shows the current filtered list."""
        for possibility in self.guess_manager.get_filtered_list():
            self.stdout.write(possibility)
            self.stdout.write("\n")

    def do_exit(self, args):
        """Exits the application."""
        return True

    def do_quit(self, args):
        """Quits the application."""
        return True

