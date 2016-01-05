from peewee import *
import unittest
from models import PayRun


class TestPayRun(unittest.TestCase):

    def setUp(self):
        self.db = SqliteDatabase('c:\\bench\\allocat\\allocat.db')

    def test_get_all(self):
        runs = PayRun.get_all()
        self.assertEqual(4, len(runs))

    def test_get_one(self):
        run = PayRun.get_one(4)
        self.assertEqual('13-16-016', str(run))

    def test_get_records(self):
        run = PayRun.get_one(4)
        self.assertEqual(85, len([rec for rec in run.records]))

    def test_get_diffs(self):
        run = PayRun.get_one(4)
        self.assertEqual(334, len([diff for diff in run.diffs]))
