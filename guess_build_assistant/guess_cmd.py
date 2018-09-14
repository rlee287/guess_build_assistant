import cmd
from .guess_manager import GuessManager

class GuessCmd(cmd.Cmd):
    helpstr = """Overview of commands:
       "help" Prints out help information
       "reset" Resets the game to begin anew.
       "len <number>" Sets the length of the word.
       "hint <number> <character>" Sets a hint position.
       "clue <number> <character>" Sets a hint position.
       Nonimpl "<number> <character>" Sets a hint position.
       "wordlist <optional path>" Prints the wordlist or
                                  sets the wordlist if path is given.
       "showlist" Shows the filtered list of possible words.
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
        self.stdout.write(self.prompt)

    def do_reset(self, args):
        """Resets the game to begin anew."""
        # Create new guess manager and cleanup old one
        self.guess_manager = GuessManager(self.wordlist)

    def do_wordlist(self, args):
        """Prints out the wordlist or sets a new one."""
        self.wordlist=args
        self.do_reset(None)

    def do_len(self, args):
        """Sets the length of the word."""
        int_len=0
        try:
            int_len=int(args)
            if int_len<=0:
                raise ValueError
            self.guess_manager.set_length(int_len)
        except ValueError:
            self.stdout.write("Error: {} is not a valid length\n"
                                    .format(repr(args)))

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
        argslist=args.split()
        if len(argslist)!=2:
            self.stdout.write("Error: args must be of the form <number> <character>\n")
            return
        int_pos=-1
        try:
            int_pos=int(argslist[0])
        except ValueError:
            self.stdout.write("Error: args must be of the form <number> <character>\n")
            return
        if len(argslist[1])>1:
            self.stdout.write("Error: args must be of the form <number> <character>\n")
            return
        if int_pos<=0 or int_pos>self.guess_manager.length:
            self.stdout.write("Error: position must be within the clue length")
            return
        if argslist[1] not in "qwertyuiopasdfghjklzxcvbnm *":
            self.stdout.write("Error: char must be a letter, space, or asterisk")
            return
        # UI is 1 based, program is 0 based
        self.guess_manager.set_clue(int_pos-1,argslist[1])

    #def default(self, line):
    #    pass

    def do_showclue(self, args):
        """Shows the current clue."""
        self.stdout.write(self.guess_manager.get_cluestr())
        self.stdout.write("\n")

    def do_showlist(self, args):
        """Shows the current list."""
        for possibility in self.guess_manager.get_filtered_list():
            self.stdout.write(possibility)
            self.stdout.write("\n")

    def do_exit(self, args):
        """Exits the application."""
        return True

    def do_quit(self, args):
        """Quits the application."""
        return True

