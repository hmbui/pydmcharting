import random
from pydm.PyQt.QtCore import Qt
from pydm.PyQt.QtGui import QColor, QMessageBox


PREDEFINED_COLORS = (Qt.red, Qt.green,  Qt.darkRed,  Qt.blue, Qt.darkGreen,  Qt.cyan,  Qt.darkBlue,  Qt.darkCyan,
                     Qt.magenta,  Qt.darkMagenta)


def random_color():
    """Return a random hex color description"""
    return QColor(random.choice(PREDEFINED_COLORS))


def display_message_box(icon, window_title, text):
    msg_box = QMessageBox()
    msg_box.setIcon(icon)
    msg_box.setWindowTitle(window_title)
    msg_box.setText(text)

    msg_box.exec_()

