from peewee import *
import unittest
from models import PayRun


class TestPayRun(unittest.TestCase):

    def setUp(self):
        self.db = SqliteDatabase('c:\\bench\\allocat\\allocat.db')

    def test_get_all(self):
        runs = PayRun.get_all()
        self.assertEqual(12, len(runs))

    def test_get_one(self):
        run = PayRun.get_one(1)
        self.assertEqual('13-15-015', str(run))
        self.assertEqual(39, len(run.records))
        self.assertEqual(0, len(run.diffs))

        run = PayRun.get_one(10)
        self.assertEqual('15-22-016', str(run))
        self.assertEqual(91, len(run.records))
        self.assertEqual(73, len(run.diffs))

    def test_get_by_tag(self):
        run = PayRun.get_by_tag('15-22-016')
        self.assertEqual('15-22-016', str(run))
        self.assertEqual(91, len(run.records))
        self.assertEqual(73, len(run.diffs))

    def test_get_previous_run_id(self):
        run = PayRun.get_by_tag('15-22-016')
        run_id = run.get_previous_run_id()
        self.assertEqual(8, run_id)

    def test_get_previous_records(self):
        run = PayRun.get_by_tag('15-23-016')
        rex = run._get_previous_records()
        self.assertEqual(91, len(rex))

    # def test_set_records(self):
    #     run = Payrun.get_one(self.db, 4)
    #     run.set_records(self.db)
    #     self.assertEqual(85, len(run.records))
    #
    # def test_get_diffs(self):
    #     run = Payrun.get_one(4)
    #     self.assertEqual(334, len([diff for diff in run.diffs]))
