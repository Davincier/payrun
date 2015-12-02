# coding=utf-8
__author__ = 'Joe'

from .rpc_exception import RpcException
from .rpc import Rpc, RpcParameter


class RpcUser(object):

    def __init__(self):
        self.access_code = None
        self.verify_code = None
        self.uid = None
        self.context = None

    def login(self, cxn, access_code, verify_code, context=None, encryption_indexes=None):
        rpc = Rpc.create('XUS SIGNON SETUP')
        response = cxn.execute(rpc)
        if response is None:
            raise RpcException('Unable to setup login')
        if encryption_indexes is None:
            param = [RpcParameter(RpcParameter.ENCRYPTED, access_code + ';' + verify_code)]
        else:
            param = [RpcParameter(RpcParameter.ENCRYPTED, access_code + ';' + verify_code, encryption_indexes)]
        rpc = Rpc.create('XUS AV CODE', param)
        response = cxn.execute(rpc)
        if response is None:
            raise RpcException('No response to login request')
        greeting = self._load(response)
        self.access_code = access_code
        self.verify_code = verify_code

        if context is not None:
            self.set_context(cxn, context, encryption_indexes)

        return greeting

    def set_context(self, cxn, context, encryption_indexes=None):
        if encryption_indexes is None:
            param = [RpcParameter(RpcParameter.ENCRYPTED, context)]
        else:
            param = [RpcParameter(RpcParameter.ENCRYPTED, context, encryption_indexes)]
        rpc = Rpc.create('XWB CREATE CONTEXT', param)
        response = cxn.execute(rpc)
        if response != '1':
            raise RpcException(response)
        self.context = context

    def _load(self, response):
        parts = response.split("\r\n")
        if parts[0] == '0':
            raise RpcException(parts[3])
        self.uid = parts[0]
        if len(parts) > 7:
            return parts[7]
        return 'OK'