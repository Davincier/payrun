__author__ = 'Joe'

from .rpc import Rpc, RpcParameter


def get_variable_value(cxn, arg):
    param = RpcParameter(RpcParameter.REFERENCE, arg)
    rpc = Rpc.create('XWB GET VARIABLE VALUE', [param])
    return cxn.execute(rpc)


def get_global_header(cxn, globl):
    arg = '$G(^%s,0))' % globl
    response = get_variable_value(cxn, arg)
    parts = response.split('^')
    return {
        'name': parts[0],
        'nbr': parts[1],
        'last_ien': parts[2],
        'nentries': parts[3]
    }


