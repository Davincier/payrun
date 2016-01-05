from peewee import *
import unittest
from models import Employee


class TestEmployee(unittest.TestCase):

    def setUp(self):
        self.db = SqliteDatabase('c:\\bench\\allocat\\allocat.db')

    def test_get_all(self):
        emps = Employee.get_all()
        self.assertEqual(163, len(emps))

    def test_get_one(self):
        emp = Employee.get_one(7)
        self.assertEqual("KERR,EVE A", emp.name)

    def test_get_records(self):
        emp = Employee.get_one(7)
        self.assertEqual(2, len([rec for rec in emp.payrecords]))

    def test_get_diffs(self):
        emp = Employee.get_one(7)
        self.assertEqual(2, len([diff for diff in emp.paydiffs]))