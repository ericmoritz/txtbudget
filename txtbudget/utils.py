from dateutil import rrule
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import date
import re
import sys


DELTA_PATTERN=re.compile("(\d*)([ymdw])(\d*)")
FREQ_MAP = {
    'y': rrule.YEARLY,
    'm': rrule.MONTHLY,
    'w': rrule.WEEKLY,
    'd': rrule.DAILY,
}


def parse_rrule(delta_str, dtstart):
    """Recurrence follows the following pattern: 
(\d*)([ymwd])(\d*)
The first group is the interval
The second group is the frequency: y=yearly,m=monthly,w=weekly,d=daily
The third group is the count since the start"""
    if delta_str == "" or delta_str is None:
        delta_str = "1d1" # If not given, it defaults to only one instance

    match = DELTA_PATTERN.match(delta_str)

    if not match:
        raise ValueError("Format is \d*[ymdw]\d*")

    interval, freq, count = match.groups()
    freq = FREQ_MAP[freq]

    try:
        interval = int(interval)
    except ValueError:
        interval = 1

    try:
        count = int(count)
    except ValueError:
        count = None

    return rrule.rrule(freq, interval=interval, count=count,
                       dtstart=dtstart)



class TransactionItem(object):
    def __init__(self, name, amount, date):
        self.name = name
        self.amount = amount
        self.date = date

    def __iter__(self):
        return iter([self.name, self.amount, self.date])

    def __unicode__(self):
        bits = list(self)
        bits[2] = bits[2].strftime("%m/%d/%Y")

        bits = map(lambda x: x or "", bits)
        bits = map(unicode, bits)        
        return ", ".join(bits)

    def __cmp__(self, other):
        return cmp((self.date, self.name, self.amount),
                   (other.date, other.name, other.amount))

        
class ScheduleItem(object):
    def __init__(self, name, amount, start, recur=None):
        self.name = name
        self.amount = amount
        self.start = start
        self.recur = recur

        self.rrule = parse_rrule(recur, self.start)

    def until(self, dtend, dtstart=None):
        if dtstart is None:
            dtstart = self.start
        
        for dt in self.rrule.between(dtstart,
                                     dtend,
                                     inc=True):
            yield (self.name, self.amount, dt)


    def __cmp__(self, other):
        t1 = (self.start, self.amount, self.name, self.recur)
        t2 = (other.start, other.amount, other.name, other.recur)

        return cmp(t1,t2)

    def __iter__(self):
        return iter([self.name, self.amount, self.start, self.recur])

    def __unicode__(self):
        bits = list(self)
        bits[2] = bits[2].strftime("%m/%d/%Y")

        bits = map(lambda x: x or "", bits)
        bits = map(unicode, bits)        
        return ", ".join(bits)

        
def schedule_parser_gen(lines):
    linenumber = 0
    for line in lines:
        linenumber = linenumber + 1
        line = line.strip()
        
        if line and line[0] != '#':
            # Take off any trailing comments
            bits = line.split("#")[0]
            # Split the items on commas
            bits = bits.split(",")

            # Strip any trailing stuff
            bits = map(lambda x: x.strip(), bits)

            name, amount, dtstart, recur = bits

            amount = float(amount)
            dtstart = parser.parse(dtstart)
            yield ScheduleItem(name, amount, dtstart, recur)        
