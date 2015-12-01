class PayEmployee(object):

    def __init__(self, name, grade, step, fte):
        self.name = name
        self.grade = grade
        self.step = step
        self.fte = fte

    def __str__(self):
        return '%s: GRADE %02d, STEP %02d, FTE %s%%' % \
               (self.name, self.grade, self.step, self.fte * 100)