import unittest
from unittest.mock import MagicMock
from PyQt5.QtWidgets import QApplication
from pymongo import MongoClient
from pyvista.rpc import RpcServer
from pyvista.fms.payrun import *
from controllers import PayrunController

app = QApplication([])

class TestPayrunController(unittest.TestCase):

    def setUp(self):
        db = MongoClient('localhost', 3001).meteor
        self.controller = PayrunController(db)

    def test_save_run(self):
        f = open('../../pyvista/fms/tests/run560_015.txt', 'rb')
        response_015 = f.read().decode()
        f.close()

        f = open('../../pyvista/fms/tests/run560_016.txt', 'rb')
        response_016 = f.read().decode()
        f.close()

        cxn = RpcServer(None, 0)
        cxn.execute = MagicMock(side_effect=[
            '560', response_015, response_016
        ])

        fms_run = FmsPayrun(cxn, '13-16')
        my_run = fms_run.get_records(['015', '016'])

        self.controller.save_run('13-16', my_run)

    def test_save_runs(self):
        f = open('../../pyvista/fms/tests/run559_015.txt', 'rb')
        response559_015 = f.read().decode()
        f.close()

        f = open('../../pyvista/fms/tests/run559_016.txt', 'rb')
        response559_016 = f.read().decode()
        f.close()

        f = open('../../pyvista/fms/tests/run560_015.txt', 'rb')
        response560_015 = f.read().decode()
        f.close()

        f = open('../../pyvista/fms/tests/run560_016.txt', 'rb')
        response560_016 = f.read().decode()
        f.close()

        f = open('../../pyvista/fms/tests/run616_015.txt', 'rb')
        response616_015 = f.read().decode()
        f.close()

        f = open('../../pyvista/fms/tests/run616_016.txt', 'rb')
        response616_016 = f.read().decode()
        f.close()

        f = open('../../pyvista/fms/tests/run617_015.txt', 'rb')
        response617_015 = f.read().decode()
        f.close()

        f = open('../../pyvista/fms/tests/run617_016.txt', 'rb')
        response617_016 = f.read().decode()
        f.close()

        f = open('../../pyvista/fms/tests/run618_015.txt', 'rb')
        response618_015 = f.read().decode()
        f.close()

        f = open('../../pyvista/fms/tests/run618_016.txt', 'rb')
        response618_016 = f.read().decode()
        f.close()

        f = open('../../pyvista/fms/tests/run619_015.txt', 'rb')
        response619_015 = f.read().decode()
        f.close()

        f = open('../../pyvista/fms/tests/run619_016.txt', 'rb')
        response619_016 = f.read().decode()
        f.close()

        cxn = RpcServer(None, 0)
        cxn.execute = MagicMock(side_effect=[
            '559', response559_015, response559_016,
            '560', response560_015, response560_016,
            '616', response616_015, response616_016,
            '617', response617_015, response617_016,
            '618', response618_015, response618_016,
            '619', response619_015, response619_016
        ])

        fms_run = FmsPayrun(cxn, '13-15')
        my_run = fms_run.get_records(['015', '016'])
        self.controller.save_run('13-15', my_run)

        fms_run = FmsPayrun(cxn, '13-16')
        my_run = fms_run.get_records(['015', '016'])
        self.controller.save_run('13-16', my_run)

        fms_run = FmsPayrun(cxn, '15-20')
        my_run = fms_run.get_records(['015', '016'])
        self.controller.save_run('15-20', my_run)

        fms_run = FmsPayrun(cxn, '15-21')
        my_run = fms_run.get_records(['015', '016'])
        self.controller.save_run('15-21', my_run)

        fms_run = FmsPayrun(cxn, '15-22')
        my_run = fms_run.get_records(['015', '016'])
        self.controller.save_run('15-22', my_run)

        fms_run = FmsPayrun(cxn, '15-23')
        my_run = fms_run.get_records(['015', '016'])
        self.controller.save_run('15-23', my_run)





