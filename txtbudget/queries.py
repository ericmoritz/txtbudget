from utils import schedule_parser_gen, TransactionItem
from six.moves import map
import itertools

def until(csv_lines, dtend, dtstart=None):
    def result_key(ti):
        return (ti.date, ti.name)

    return sorted(
        (
            TransactionItem(*x)
            for si in schedule_parser_gen(csv_lines)
            for x in si.until(dtend, dtstart=dtstart)
        ),
        key=result_key
    )
    

    gen = schedule_parser_gen(csv_lines)
    gen = (si.until(dtend, dtstart=dtstart) for si in gen)
    gen = itertools.chain(*gen)
    gen = (TransactionItem(*x) for x in gen)
    return sorted(gen, key=result_key)


