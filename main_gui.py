from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from ids.ids_gui import IDSGUI
from permissions.permission_gui import PermissionGUI
from traffic.traffic_gui import TrafficGUI  # ✅ Correct class name

class MainGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Security Toolkit")
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet("background-color: #222; color: white;")

        layout = QVBoxLayout()

        title = QLabel("Network Security Monitoring")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.ids_button = QPushButton("Intrusion Detection System")
        self.permission_button = QPushButton("Permission Detection")
        self.traffic_button = QPushButton("Real-Time Traffic Monitoring")

        for btn in [self.ids_button, self.permission_button, self.traffic_button]:
            btn.setFixedHeight(50)
            btn.setFont(QFont("Segoe UI", 12))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #007acc;
                    border-radius: 8px;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #005f9e;
                }
            """)
            layout.addWidget(btn)

        self.setLayout(layout)

        self.ids_button.clicked.connect(self.open_ids)
        self.permission_button.clicked.connect(self.open_permission)
        self.traffic_button.clicked.connect(self.open_traffic)

    def open_ids(self):
        self.ids = IDSGUI()
        self.ids.show()

    def open_permission(self):
        self.permission = PermissionGUI()
        self.permission.show()

    def open_traffic(self):
        self.traffic = TrafficGUI()  # ✅ Corrected from TrafficMonitor to TrafficGUI
        self.traffic.show()
