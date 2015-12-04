def main():
    import sys
    from pymongo import MongoClient
    from PyQt5.QtWidgets import QApplication
    import qdarkstyle
    from controllers import PayrunController

    db = MongoClient('localhost', 3001).meteor

    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    ctrlr = PayrunController(db)
    ctrlr.runit()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
