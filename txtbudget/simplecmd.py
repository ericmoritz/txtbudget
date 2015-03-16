import sys
import os.path
import readline
import atexit
import rlcompleter

class InvalidArgs(Exception):
    pass


def help(config, args):
    """List out help for the commands"""
    COMMAND_MAP = config['cmd_mapping']

    if len(args) > 0:
        cmd_list = args
    else:
        cmd_list = COMMAND_MAP.keys()
    for cmd in cmd_list:
        print "Help for '%s':" % (cmd, )
        if cmd in COMMAND_MAP and cmd.__doc__:
            func = COMMAND_MAP[cmd]
            if func.__doc__:
                print func.__doc__
            else:
                print "Command has no help"
        else:
            print "Can't find command"
        print "\n"


def quit(config, args):
    """Quits"""
    print "bye.\n"
    sys.exit(0)

DEFAULT_MAP = {
    "help": help,
    "quit": quit,

}

def parse_line(line):
    bits = line.split()
    cmd = bits[0]
    args = bits[1:]
    return (cmd, args)

class SimpleCompleter(object):
    def __init__(self, config):
        self.config = config
        self.cmd_mapping = config['cmd_mapping']

    def complete(self, text, state):
        matches = [key for key in self.cmd_mapping \
                       if key.startswith(text)]
        if len(matches) == 1:
            return [matches[0], None][state]

def simplecmd(COMMAND_MAP, line=None, config=None,
              histfile=None):
    cmd_mapping = dict(**DEFAULT_MAP)
    cmd_mapping.update(COMMAND_MAP)
    
    config = config or {}
    config['cmd_mapping'] = cmd_mapping

    if histfile:
        histfile = os.path.expanduser(histfile)

    try:
        readline.read_history_file(histfile)
    except IOError:
        pass

    atexit.register(readline.write_history_file, histfile)

    readline.parse_and_bind("tab: complete")
    readline.set_completer(SimpleCompleter(config).complete)

    def rawinput_gen():

        while True:
            try:
                line = raw_input(":")
                yield line
            except (KeyboardInterrupt, EOFError):
                print
                cmd_mapping["quit"](config,[])

    def oneinput_gen(line):
        yield line


    if line:
        cmd_gen = oneinput_gen(line)
    else:
        cmd_gen = rawinput_gen()

    for line in cmd_gen:
        cmd, args = parse_line(line)

        # Try to do a substring match
        if cmd not in cmd_mapping:
            match = [key for key in cmd_mapping.keys() if key.startswith(cmd)]

            # Only allow substring match if only one matches
            if len(match) == 1:
                cmd = match[0]
            else:
                cmd = None

        # If the cmd is in the mapping
        if cmd:
            # fire it off
            try:
                cmd_mapping[cmd](config, args)
            except SystemExit:
                break
            except Exception, e:
                print str(e)

        else:
            print "Command not found.\n"
