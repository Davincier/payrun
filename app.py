def main():
    import sys
    from pymongo import MongoClient
    from PyQt5.QtWidgets import QApplication
    from controllers.payrun_controller import PayrunController

    db = MongoClient('localhost', 3001).meteor

    app = QApplication(sys.argv)
    ctrlr = PayrunController(db)
    ctrlr.runit()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
