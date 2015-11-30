__author__ = 'Joe'

def clearLayout(layout):
    while layout.count() > 0:
        item = layout.takeAt(0)
        if not item:
            continue
        w = item.widget()
        if w:
            w.deleteLater()