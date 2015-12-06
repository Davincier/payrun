import unittest
from pyvista.rpc import RpcServer, RpcParameter, Rpc


class TestRpc(unittest.TestCase):

    def setUp(self):
        self.cxn = RpcServer(None, 0)

    def test_payrun_ien_rpc(self):
        pay_period = '15-22'
        arg = '$O(^PRST(459,"B","%s",1))' % (pay_period)
        param = RpcParameter(RpcParameter.REFERENCE, arg)
        rpc = Rpc.create('XWB GET VARIABLE VALUE', [param])

        expected = "[XWB]113021.108XWB GET VARIABLE VALUE51028$O(^PRST(459,\"B\",\"15-22\",1))f"
        self.assertEqual(rpc, expected)
