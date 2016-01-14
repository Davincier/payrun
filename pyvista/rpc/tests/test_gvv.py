import unittest
from unittest.mock import MagicMock
from pyvista.rpc import RpcServer
from pyvista.rpc.gvv import *


class TestGetVariableValue(unittest.TestCase):

    def setUp(self):
        self.cxn = RpcServer(None, 0)

    def test_get_variable_value(self):
        # Rpc.create = MagicMock()
        # self.cxn.execute = MagicMock(return_value='')
        pass

    # This is because the linter can't find assert_called_with
    # noinspection PyUnresolvedReferences
    def test_get_global_header(self):
        globl = 'PRST(459'
        self.cxn.execute = MagicMock(return_value='PAID PAYRUN DATA^459^612^612')
        expected = {
            'name': 'PAID PAYRUN DATA',
            'nbr': '459',
            'last_ien': '612',
            'nentries': '612'
        }
        result = get_global_header(self.cxn, globl)
        rpc = "[XWB]11302\x051.108\x16XWB GET VARIABLE VALUE51016$G(^PRST(459,0))f\x04"
        self.cxn.execute.assert_called_with(rpc)
        self.assertEqual(result, expected)
