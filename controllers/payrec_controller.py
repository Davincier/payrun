from app import rec_fields
from views import PayrecWidget


class PayrecController(object):
    def __init__(self, payrun, payrec):
        self.widget = PayrecWidget()
        self.widget.load_record(payrun, payrec, rec_fields)

    def runit(self):
        self.widget.exec_()
