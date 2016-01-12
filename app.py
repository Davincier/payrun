from peewee import SqliteDatabase

db = SqliteDatabase('c:\\bench\\allocat\\allocat.db')
diff_fields = [f.name for f in db.get_columns('payrecords')]
rec_fields = diff_fields[3:-1]


def main():
    import sys
    from PyQt5.QtWidgets import QApplication
    from controllers import PayrunController

    app = QApplication(sys.argv)
    ssh_file = 'views/allocat.stylesheet'
    with open(ssh_file, "r") as fh:
        app.setStyleSheet(fh.read())

    ctrlr = PayrunController()
    ctrlr.runit()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
