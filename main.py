from PyQt5.QtWidgets import QApplication
from gui.main_gui import MainGUI
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainGUI()
    window.show()
    sys.exit(app.exec_())
