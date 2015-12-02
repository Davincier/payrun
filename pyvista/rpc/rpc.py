# coding=utf-8
__author__ = 'Joe'

from .utils import *
from .rpc_exception import RpcException


class Rpc(object):

    PREFIX = '[XWB]'
    COUNT_WIDTH = 3
    RPC_VERSION = '1.108'
    EOT = "\x04"

    def __init__(self, name, params=None):
        self.name = name
        self.params = params

    @classmethod
    def create(cls, name, params=None):
        rpc = Rpc(name, params)
        return rpc._prepare()

    def _prepare(self):
        if self.name == 'HELLO':
            return self._connect_rpc()
        if self.name == 'BYE':
            return self._disconnect_rpc()
        return self._prepare_standard_rpc()

    def _prepare_standard_rpc(self):
        params = [
            self.PREFIX,
            '11302',
            prepend_count(self.RPC_VERSION),
            prepend_count(self.name),
            self._prepare_param_str(),
            self.EOT
        ]
        return ''.join(params)

    def _list_to_string(self, param_list):
        if not len(param_list):
            return str_pack('', self.COUNT_WIDTH) + 'f'

        param_string = ""
        for param in param_list:
            if param[1] == "":
                param[1] = "\x01"
            param_string = ''.join(
                [
                    param_string,
                    str_pack(param[0], self.COUNT_WIDTH),
                    str_pack(param[1], self.COUNT_WIDTH), 't'
                ]
            )
        return param_string[0:-1] + 'f'

    def _prepare_param_str(self):
        param_str = '5'
        if self.params:
            for param in self.params:
                if param.type == RpcParameter.LITERAL:
                    param_str = ''.join([param_str, '0', str_pack(param.value, self.COUNT_WIDTH), 'f'])
                elif param.type == RpcParameter.REFERENCE:
                    param_str = ''.join([param_str, '1', str_pack(param.value, self.COUNT_WIDTH), 'f'])
                elif param.type == RpcParameter.LIST:
                    param_str = ''.join([param_str, '2', self._list_to_string(param.value)])
                else:
                    raise RpcException('Invalid param type')
        if param_str == '5':
            param_str += '4f'
        return param_str

    def _connect_rpc(self):
        return ''.join([
            "[XWB]10304\x0ATCPConnect50",
            str_pack(self.params[0].value, self.COUNT_WIDTH),
            "f0", str_pack('0', self.COUNT_WIDTH),
            "f0", str_pack(self.params[1].value, self.COUNT_WIDTH),
            "f", self.EOT])

    def _disconnect_rpc(self):
        return "[XWB]10304\x05#BYE#" + self.EOT


class RpcParameter(object):

    LITERAL = 1
    REFERENCE = 2
    LIST = 3
    WORDPROC = 4
    ENCRYPTED = 10

    TYPES = [LITERAL, REFERENCE, LIST, WORDPROC, ENCRYPTED]

    def __init__(self, param_type, value, encryption_indexes=None):
        if param_type not in self.TYPES:
            raise RpcException("Invalid param type")
        self.type = self.LITERAL if param_type == self.ENCRYPTED else param_type
        if param_type != self.ENCRYPTED:
            self.value = value
        elif encryption_indexes is None:
            self.value = encrypt(value)
        else:
            self.value = encrypt(value, encryption_indexes)
