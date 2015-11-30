class PayEmployee(object):

    def __init__(self, name, grade, step, fte):
        self.name = name
        self.grade = grade
        self.step = step
        self.fte = fte

    def __str__(self):
        return self.name

    def gfs(self):
        return 'GRADE: %02d, STEP: %02d, FTE: %s' % \
               (self.grade, self.step, self.fte)