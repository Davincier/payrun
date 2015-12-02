__author__ = 'Joe'

from pyvista.rpc import DdrLister


fieldDefs = [
    ('.01E', 'EMPLOYEE NAME'),
    ('13', 'GRADE'),
    ('38', 'STEP'),
    ('450', 'FTE')
]

fields = [f[0] for f in fieldDefs]
fieldnames = [f[1] for f in fieldDefs]
fieldnames.insert(0, 'EMPLOYEE UID')


def get_by_cost_center(cxn, cost_center):
    query = DdrLister()
    query.file = '450'
    query.fields = ';'.join(fields)
    query.index = 'ACC'
    query.frum = cost_center
    query.part = cost_center
    query.fieldnames = fieldnames
    return query.find(cxn)