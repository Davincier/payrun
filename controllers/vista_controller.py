from pyvista.rpc import RpcServer, RpcVisitor
from pyvista.fms import FmsPayrun


class VistaController(object):

    def __init__(self):
        self._set_vista_params()

    def _set_vista_params(self):
        import json
        with open("controllers/config.json") as cfg_file:
            data = json.load(cfg_file)

        self.host = data['vista']['host']
        self.port = data['vista']['port']
        self.user = {
            "fed_id": data['vista']['user']['fed_id'],
            "user_name": data['vista']['user']['name'],
            "source_name": data['vista']['site_name'],
            "source_id": data['vista']['site_id'],
            "uid": data['vista']['user']['uid'],
            "phone": data['vista']['user']['phone']
        }
        self.cps = data['control_points']

    def _connect(self):
        svr = RpcServer(self.host, self.port)
        svr.open()
        if not svr.is_open:
            msg = 'Unable to connect to %s, port %d' % (self.host, self.port)
            raise Exception(msg)
        visitor = RpcVisitor(self.user)
        visitor.visit(svr)
        return svr

    def get_payrun_records(self, pay_period):
        cxn = self._connect()
        run = FmsPayrun(cxn, pay_period)
        rex = run.get_records(self.cps)
        cxn.close()
        return rex
