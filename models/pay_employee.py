class PayEmployee(object):

    def __init__(self, name, grade, step, fte):
        self.name = name
        self.grade = int(grade)
        self.step = int(step)
        self.fte = int(float(fte) * 100)

    def __str__(self):
        return '%s: GRADE %02d, STEP %02d, FTE %s%%' % \
               (self.name, self.grade, self.step, self.fte)