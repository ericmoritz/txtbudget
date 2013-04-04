from utils import *
from simplecmd import simplecmd, InvalidArgs
from dateutil import rrule
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import date
from config import load_config, json_config
from functools import partial
import os
import re
import sys


def balance(config, args):
    """Lists out scheduled transactions between two dates
Usage:
list [start] [end] - lists transactions between two dates
list [end] - lists out transactions from their start until today
list [month number] - list out the transactions for a month
"""
    import codecs
    import itertools

    schedule_filename = config['filename']
    dates = args
    month_start = int(config.get("month_start", 1))

    if len(dates) == 2:
        dtstart = parser.parse(dates[0])
        dtend   = parser.parse(dates[1])
    elif len(dates) <= 1:
        try:
            # Try to do the single month shortcut
            try:
                month = int(dates[0])
            except IndexError:
                month = date.today().month

            dtstart = parser.parse("%s/%s" % (month, month_start))
            dtend = dtstart + relativedelta(months=1) - relativedelta(days=1)
        except ValueError:
            dtstart = None
            dtend = parser.parse(dates[0])
    else:
        raise InvalidArgs("""usage: list [start date] [end date]
list [end date]
list [month number]
list""")


    fh = codecs.open(schedule_filename, "r", "utf-8")

    gen = schedule_parser_gen(fh)
    gen = (si.until(dtend, dtstart=dtstart) for si in gen)
    gen = itertools.chain(*gen)
    gen = (TransactionItem(*x) for x in gen)

    # Sort the result
    result = sorted(gen)

    # Locals is used by the ! command to define it's locals
    config['locals'] = {'r': [(i.name, i.amount, i.date) for i in result]}

    # Get the sum
    total = sum((ti.amount for ti in result))

    # Print the result
    print u"-"*79
    total = 0
    for i, item in enumerate(result):
        total = total + item.amount
        print u"%.2f: %s. %s" % (total, i, item)
    print u"-"*79
    print u"%d" % (total, )

def pycmd(config, args):
    from pprint import pprint
    cmd = " ".join(args)

    pprint(eval(cmd, {}, config.get("locals", {})))


COMMAND_MAP = {
    "list": balance,
    "!": pycmd
}


def main():
    def arg_config():
        return {
            'filename': sys.argv[1]
        }

    config = load_config([
        partial(
            json_config,
            os.path.expanduser("~/.txtbudget.json")
        ),
        partial(
            json_config,
            os.path.abspath("./.txtbudget.json")
        ),
        arg_config
    ])

    if len(sys.argv) > 2:
        line = " ".join(sys.argv[2:])
        simplecmd(COMMAND_MAP,config=config,
                  histfile="~/.pybudget.hist",
                  line=line)
    else:
        simplecmd(COMMAND_MAP,config=config,
                  histfile="~/.pybudget.hist",)
