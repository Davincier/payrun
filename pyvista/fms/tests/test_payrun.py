import unittest
from unittest.mock import MagicMock, call
from pyvista.rpc import RpcServer
from pyvista.fms.payrun import *


class TestPayrun(unittest.TestCase):

    def test_get_vista_field_str(self):
        run = FmsPayrun(None, '')
        fields = run._get_vista_field_str()
        expected = ".01E;3;4;10;6;11;29;34;37;40;61;63;64;66;85;88;94;118;131;132;133;134;135;136;137;138"
        self.assertEqual(fields, expected)

    def test_get_fieldnames(self):
        run = FmsPayrun(None, '')
        fieldnames = run._get_fieldnames()
        expected = [
            'EMPLOYEE UID',
            'EMPLOYEE',
            'GRADE',
            'STEP',
            'FTE',
            '8B NORMAL HOURS',
            'NORMAL HOURS',
            'OASDI TAX VA SHARE CPPD',
            'FEGLI VA SHARE CPPD',
            'HEALTH BENEFITS VA SHARE CPPD',
            'RETIREMENT VA SHARE CPPD',
            'TSP CSF GOV BASIC CONTRIB',
            'TSP GSF GOV BASIC CONTRIB',
            'TSP CSF GOV MATCH CONTRIB',
            'TSP GSF GOV MATCH CONTRIB',
            'BASE PAY CPPD',
            'HOLIDAY AMT',
            'OVERTIME AMT CPPD',
            'GROSS PAY PLUS BENEFITS CPPD',
            'OVERTIME HOURS WK 1',
            'OVERTIME HOURS WK 2',
            'OVERTIME AMT WK 1',
            'OVERTIME AMT WK 2',
            'HRS EXCESS 8 DAY WK 1',
            'HRS EXCESS 8 DAY WK 2',
            'HRS EXCESS 8 DAY AMT WK 1',
            'HRS EXCESS 8 DAY AMT WK 2'
        ]
        self.assertEqual(fieldnames, expected)

    def test_payrun_ien_rpc(self):
        pay_period = '15-22'
        arg = '$O(^PRST(459,"B","%s",1))' % (pay_period)
        param = RpcParameter(RpcParameter.REFERENCE, arg)
        rpc = Rpc.create('XWB GET VARIABLE VALUE', [param])

        expected = "[XWB]113021.108XWB GET VARIABLE VALUE51028$O(^PRST(459,\"B\",\"15-22\",1))f"
        self.assertEqual(rpc, expected)

        pay_period = '15-23'
        arg = '$O(^PRST(459,"B","%s",1))' % (pay_period)
        param = RpcParameter(RpcParameter.REFERENCE, arg)
        rpc = Rpc.create('XWB GET VARIABLE VALUE', [param])

        expected = "[XWB]113021.108XWB GET VARIABLE VALUE51028$O(^PRST(459,\"B\",\"15-23\",1))f"
        self.assertEqual(rpc, expected)

    def test_get_ien(self):
        cxn = RpcServer(None, 0)
        cxn.execute = MagicMock(return_value='618')
        run = FmsPayrun(cxn, '15-22')
        ien = run._get_ien()
        self.assertEqual(ien, '618')

    def test_payrun_rpc(self):
        run = FmsPayrun(None, 0)
        run.ien = '618'
        query = run._build_query('015')
        query._prepare()

        expected = "[XWB]113021.108\nDDR LISTER52006\"FILE\"006459.01t006\"IENS\"005,618,t008\"FIELDS\"087@;.01E;3;4;10;6;11;29;34;37;40;61;63;64;66;85;88;94;118;131;132;133;134;135;136;137;138t007\"FLAGS\"002IPt006\"XREF\"001Bt008\"SCREEN\"021I $P(^(0),U,10)=\"015\"f"
        self.assertEqual(query.rpc, expected)

    def test_get(self):
        rpcs = [
            call("[XWB]113021.108XWB GET VARIABLE VALUE51028$O(^PRST(459,\"B\",\"15-22\",1))f"),
            call("[XWB]113021.108\nDDR LISTER52006\"FILE\"006459.01t006\"IENS\"005,618,t008\"FIELDS\"087@;.01E;3;4;10;6;11;29;34;37;40;61;63;64;66;85;88;94;118;131;132;133;134;135;136;137;138t007\"FLAGS\"002IPt006\"XREF\"001Bt008\"SCREEN\"021I $P(^(0),U,10)=\"015\"f"),
            call("[XWB]113021.108\nDDR LISTER52006\"FILE\"006459.01t006\"IENS\"005,618,t008\"FIELDS\"087@;.01E;3;4;10;6;11;29;34;37;40;61;63;64;66;85;88;94;118;131;132;133;134;135;136;137;138t007\"FLAGS\"002IPt006\"XREF\"001Bt008\"SCREEN\"021I $P(^(0),U,10)=\"016\"f")
        ]

        f = open('run618_015.txt', 'rb')
        response_015 = f.read().decode()
        f.close()

        f = open('run618_016.txt', 'rb')
        response_016 = f.read().decode()
        f.close()

        cxn = RpcServer(None, 0)
        cxn.execute = MagicMock(side_effect=[
            '618', response_015, response_016
        ])

        run = FmsPayrun(cxn, '15-22')
        rex = run.get(['015', '016'])
        self.assertEqual(cxn.execute.call_args_list, rpcs)
        self.assertEqual(len(rex), 2)
        self.assertEqual(len(rex['015']), 39)
        self.assertEqual(len(rex['016']), 91)
