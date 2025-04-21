from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PyQt5.QtCore import QTimer
import random

class IDSGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Intrusion Detection System")
        self.setGeometry(200, 200, 500, 300)

        layout = QVBoxLayout()
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.generate_log)
        self.timer.start(2000)

    def generate_log(self):
        log = f"[ALERT] Suspicious activity detected from IP 192.168.{random.randint(1,255)}.{random.randint(1,255)}"
        self.output.append(log)
