from utils import *
from simplecmd import simplecmd, InvalidArgs
from dateutil import rrule
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import date
from config import load_config, json_config
from functools import partial
import itertools
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

    def result_key(ti):
        return (ti.date, ti.name)

    # Sort the result
    result = sorted(gen, key=result_key)

    # Locals is used by the ! command to define it's locals
    config['locals'] = {'r': [(i.name, i.amount, i.date) for i in result]}

    # Print the result
    print u"-"*79
    output_result(result)


def output_result(result):
    def columns(state, item):
        total, items = state
        total += item.amount
        items.append([total] + list(item))
        return (total, items)

    def rows():
        _, rows_ = reduce(
            columns,
            result,
            (0, []),
        )
        return rows_
        
    # returns the max string width of all strings in the table
    def width(rows):
        def w(x):
            if isinstance(x, basestring):
                return len(x)
            else:
                return 0
        return max(
            map(
                w,
                itertools.chain.from_iterable(rows)
            )
        )

    # serialize a column
    def show_column(width, x):
        if type(x) is float:
            if x < 0:
                wrap = "({:.2f})"
            else:
                wrap = "{:.2f} "
            
            return u"{:>9}".format(wrap.format(abs(x)))
        elif hasattr(x, "strftime"):
            s =  x.strftime("%m/%d/%Y")
        else:
            s = unicode(x)

        return u"{:<{width}}".format(s, width=width)

    def show_row(width, row):
        return " | ".join(map(
            partial(show_column, width),
            row
        ))

    rows_  = rows()
    width_ = width(rows_)
    rows_str = map(
            partial(show_row, width_),
            rows_
    )
    for i, r in enumerate(rows_str):
        print "{:>3} | {}".format(i, r)
        
    

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
