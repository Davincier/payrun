from pyvista.rpc import RpcServer, RpcVisitor, RpcException, VistaToken
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
        token = data['vista']['token']
        vparams = VistaToken.decrypt(token)
        if vparams.site_id != data['vista']['site_id']:
            raise RpcException('Invalid vparams')
        self.user = {
            "fed_id": vparams.fed_id,
            "user_name": vparams.username,
            "source_name": data['vista']['site_name'],
            "source_id": vparams.site_id,
            "uid": vparams.duz,
            "phone": 'No phone'
        }
        self.cps = data['control_points']

    def _connect(self):
        svr = RpcServer(self.host, self.port)
        svr.open()
        if not svr.is_open:
            msg = 'Unable to connect to %s, port %d' % (self.host, self.port)
            raise RpcException(msg)
        visitor = RpcVisitor(self.user)
        visitor.visit(svr)
        return svr

    def get_payrun_records(self, pay_period):
        cxn = self._connect()
        run = FmsPayrun(cxn, pay_period)
        rex = run.get_records(self.cps)
        cxn.close()
        return rex
