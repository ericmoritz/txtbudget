import unittest
import utils as budget
from datetime import datetime

class CreateRRule(unittest.TestCase):

    def test_all(self):
        fixture=u"2w2"
        start = datetime(2010, 3, 5)
        rrule = budget.parse_rrule(fixture,start)
        result = list(rrule)
        expect = [datetime(2010, 3, 5),
                  datetime(2010, 3, 19),]

        self.assertEqual(expect, result)

    def test_interval(self):
        fixture=u"2w"
        start = datetime(2010, 3, 5)
        rrule = budget.parse_rrule(fixture, start)
        result = rrule[0:3]
        expect = [datetime(2010, 3, 5),
                  datetime(2010, 3, 19),
                  datetime(2010, 4, 2), ]
        
        self.assertEqual(expect, result)

    def test_count(self):
        fixture = u"w2"
        start = datetime(2010, 3, 5)
        rrule = budget.parse_rrule(fixture, start)
        result = list(rrule)
        expect = [datetime(2010, 3, 5),
                  datetime(2010, 3, 12),]
        
        self.assertEqual(expect, result)


    def test_freq(self):
        fixture = u"w"
        start = datetime(2010, 3, 5)
        rrule = budget.parse_rrule(fixture, start)
        result = rrule[0:3]
        expect = [datetime(2010, 3, 5),
                  datetime(2010, 3, 12),
                  datetime(2010, 3, 19), ]
        
        self.assertEqual(expect, result)


class TestScheduleParserGen(unittest.TestCase):
    def test_comment(self):
        fixture = [u"# This is a comment",
                   u" # This is one as well", 
                   u"",
                   u"   ",
                   u"Name1, 20.10, 04/13/2010, # Comment"]

        result = list(budget.schedule_parser_gen(fixture))
        expect = [budget.ScheduleItem(u"Name1",
                                      20.10,
                                      datetime(2010,4,13),
                                      u"")]
        self.assertEqual(expect, result)


    def test_valid_line(self):
        fixture = [u"Name1, 20.10, 04/13/2010, ",
                   u"Name2, 21.01, 04/14/2010, 2w",]
        result = list(budget.schedule_parser_gen(fixture))
        expect = [budget.ScheduleItem(u"Name1",
                                      20.10,
                                      datetime(2010,4,13),
                                      u""),
                  budget.ScheduleItem(u"Name2",
                                      21.01,
                                      datetime(2010,4,14),
                                      u"2w"),]

        result = map(lambda x,y: cmp(x,y) == 0, result, expect)

        self.assertTrue(all(result), result)


class TestScheduleItem(unittest.TestCase):
    def test_iter1(self):
        fixture = budget.ScheduleItem(u"Name",
                                      20.10,
                                      datetime(2010, 4, 13),
                                      u"2w")
        expect = [u"Name", 20.10, datetime(2010, 4, 13), u"2w"]
        result = list(fixture)

        self.assertEqual(result)

    def test_iter1(self):
        fixture = budget.ScheduleItem(u"Name",
                                      20.10,
                                      datetime(2010, 4, 13),
                                      None)
        expect = [u"Name", 20.10, datetime(2010, 4, 13), None]
        result = list(fixture)

        self.assertEqual(expect, result)

    def test_unicode(self):
        fixture = budget.ScheduleItem(u"Name",
                                      20.10,
                                      datetime(2010, 4, 13),
                                      u"2w")
        expect = u"Name, 20.1, 04/13/2010, 2w"
        result = unicode(fixture)

        self.assertEqual(expect, result)

    def test_unicode(self):
        fixture = budget.ScheduleItem(u"Name",
                                      20.10,
                                      datetime(2010, 4, 13),
                                      None)
        expect = u"Name, 20.1, 04/13/2010, "
        result = unicode(fixture)

        self.assertEqual(expect, result)

    def test_until_withrrule(self):
        fixture = budget.ScheduleItem(u"Name",
                                      20.10,
                                      datetime(2010, 3, 5),
                                      u"2w")
        expect = [(u'Name', 20.10, datetime(2010, 3, 5)),
                  (u'Name', 20.10, datetime(2010, 3, 19)), ]
        
        result = list(fixture.until(datetime(2010, 3, 19)))

        self.assertEqual(expect, result)


    def test_until_withoutrrule(self):
        fixture = budget.ScheduleItem(u"Name",
                                      20.10,
                                      datetime(2010, 3, 5),
                                      u"")
        expect = [(u'Name', 20.10, datetime(2010, 3, 5)),]
        
        result = list(fixture.until(datetime(2010, 3, 19)))

        self.assertEqual(expect, result)



class TestTransactionItem(unittest.TestCase):
    def test_iter(self):
        fixture = budget.TransactionItem(u"Name",
                                         20.10,
                                         datetime(2010, 3, 15))
        expect = [u"Name", 20.10, datetime(2010, 3, 15)]
        result = list(fixture)
        
        self.assertEqual(expect, result)


    def test_unicode(self):
        fixture = budget.TransactionItem(u"Name",
                                         20.10,
                                         datetime(2010, 3, 15))
        expect = u"Name, 20.1, 03/15/2010"
        result = unicode(fixture)
        
        self.assertEqual(expect, result)
        
if __name__ == '__main__':
    unittest.main()
        
