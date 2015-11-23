__author__ = 'Joe'


def import_data(sql_db, mongo_db):
    tbl = 'efms_pay_runs'
    sql = 'select * from ' + tbl
    sql_payruns = get_sql_data(sql_db, tbl, sql)
    for sql_run in sql_payruns:
        json_run = {
            'ien': sql_run['ien'],
            'fy': sql_run['fy'],
            'pay_period': sql_run['pay_period'],
            'cp_nbr': sql_run['cp_nbr'],
            'rex': [],
            'diffs': []
        }

        tbl = 'efms_pay_run_records'
        sql = 'select * from ' + tbl + ' where payrun_id=' + str(sql_run['id'])
        json_run['rex'] = get_sql_data(sql_db, tbl, sql)

        tbl = 'efms_pay_run_diffs'
        sql = 'select * from ' + tbl + ' where payrun_id=' + str(sql_run['id'])
        json_run['diffs'] = get_sql_data(sql_db, tbl, sql)

        mongo_db.payruns.insert(json_run)


def get_sql_data(db, table, sql):
    fldnames = [f.name for f in db.get_columns(table)]
    rex = db.execute_sql(sql).fetchall()
    return [dict(zip(fldnames, rec)) for rec in rex]


if __name__ == '__main__':
    from peewee import *
    from pymongo import MongoClient

    sql_db = SqliteDatabase('rdt.db')
    mongo_db = MongoClient('localhost', 3001).meteor

    import_data(sql_db, mongo_db)

    print('Done')
