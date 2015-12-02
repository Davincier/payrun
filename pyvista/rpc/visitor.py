# coding=utf-8
__author__ = 'Joe'

from .rpc_exception import RpcException
from .rpc import Rpc, RpcParameter


class RpcVisitor(object):

    REQUIRED_FIELDS = [
        'fed_id',
        'user_name',
        'source_name',
        'source_id',
        'uid'
    ]

    def __init__(self, params):
        missing_flds = []
        for fld in self.REQUIRED_FIELDS:
            if fld not in params:
                missing_flds.append(fld)
        if missing_flds:
            raise RpcException('Cannot visit without fields: ' + ', '.join(missing_flds))

        if 'phone' not in params:
            params['phone'] = 'No phone'
        self.params = params
        self.response = None

    def _build_arg(self):
        return '-31^DVBA_^{}^{}^{}^{}^{}^{}'.format(
            self.params['fed_id'],
            self.params['user_name'],
            self.params['source_name'],
            self.params['source_id'],
            self.params['uid'],
            self.params['phone']
        )

    def visit(self, cxn):
        arg = self._build_arg()
        param = [RpcParameter(RpcParameter.LITERAL, arg)]
        rpc = Rpc.create('XUS SIGNON SETUP', param)
        self.response = cxn.execute(rpc)
        if not self._successful():
            raise RpcException('Unable to visit system {}'.format(cxn.host))
        from .user import RpcUser
        from .constants import CONTEXTS
        user = RpcUser()
        user.set_context(cxn, CONTEXTS['CAPRI'])

    def _successful(self):
        flds = self.response.split("\r\n")
        return flds[5] == '1'
