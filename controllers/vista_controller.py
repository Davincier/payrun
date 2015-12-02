from pyvista.rpc import RpcServer, RpcVisitor
from pyvista.fms.payrun import get_pay_run_ien, get_multi_payrun_records


host = None
port = -1
user = None
cps = None


def _get_vista_params():
    import json
    with open("controllers/config.json") as cfg_file:
        data = json.load(cfg_file)

    global host, port, user, cps
    host = data['vista']['host']
    port = data['vista']['port']
    user = {
        "fed_id": data['vista']['user']['fed_id'],
        "user_name": data['vista']['user']['name'],
        "source_name": data['vista']['site_name'],
        "source_id": data['vista']['site_id'],
        "uid": data['vista']['user']['uid'],
        "phone": data['vista']['user']['phone']
    }
    cps = data['control_points']


def _connect(self, host, port, user):
    svr = RpcServer(host, port)
    svr.open()
    if not svr.is_open:
        msg = 'Unable to connect to %s, port %d' % (host, port)
        raise Exception(msg)
    visitor = RpcVisitor(user)
    visitor.visit(svr)
    return svr

def get_payrun(run_id):
    _get_vista_params()
    cxn = _connect(host, port, user)
    ien = get_pay_run_ien(cxn, run_id)
    run = get_multi_payrun_records(cxn, ien, cps)
    cxn.close()
    return run
