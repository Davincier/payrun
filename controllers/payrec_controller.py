from views import PayrecWidget


class PayrecController(object):
    def __init__(self, payrun, payrec):
        self.widget = PayrecWidget()
        self.widget.load_record(payrun, payrec)

    def runit(self):
        self.widget.exec_()
