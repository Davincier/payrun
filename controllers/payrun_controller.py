from models import PayRun, PayRecord
from views import PayrunWidget, PayDiffsWidget


class PayrunController(object):
    def __init__(self):
        self.widget = PayrunWidget(self)
        self.payruns = None
        self.run = None
        self.load_payruns()

    def load_payruns(self):
        self.payruns = PayRun.get_all()
        if self.payruns.exists():
            self.widget.load_payruns(self.payruns)
            self.widget.select_payrun(0)

    def payrun_selected(self, tag_str):
        self.run = self.get_run(tag_str)
        self.load_employees()
        # self.widget.add_diffs_widget(PayDiffsWidget(self.run.diffs))

    def get_run(self, tag_str):
        tag = PayRun.get_tag(tag_str)
        return self.payruns.select().where(
            (PayRun.fy == tag.fy) &
            (PayRun.pp == tag.pp) &
            (PayRun.cp == tag.cp)
        ).get()

    def load_employees(self):
        if not self.run:
            return
        employee_names = [rec.employee.name for rec in self.run.records]
        self.widget.load_employees(employee_names)

    def employee_selected(self, employee_name):
        from models import Employee
        rec = self.run.records.select().join(Employee).where(Employee.name == employee_name)
        if not rec.exists():
            return
        from controllers import PayrecController
        controller = PayrecController(str(self.run), rec.get())
        controller.runit()

    def runit(self):
        self.widget.show()

    def add_run_clicked(self, latest_run_tag):
        latest_run = self.get_run(latest_run_tag)
        run_tag = latest_run.next_tag()
        pay_period = PayRun.pay_period(run_tag)

        from controllers import VistaController
        vc = VistaController()
        self.save_run(vc.get_payrun_records(pay_period))

    def save_run(self, pay_period, run):
        for cp in run:
            tag = '%s-%s' % (pay_period, cp)
            for rec in run[cp]:
                rec['PAYRUN'] = tag
                self.db.payrun_records.insert(rec)
            payrun = PayRun(self.db, {'tag': tag})
            payrun.rex = run[cp]
            payrun.make_diffs()
            payrun.save()
