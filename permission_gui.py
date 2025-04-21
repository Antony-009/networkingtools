import sys
import psutil
import threading
import time

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QApplication, QTextEdit, QHBoxLayout
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QColor, QBrush

class PermissionGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 Real-Time Permission Monitor")
        self.setGeometry(100, 100, 800, 500)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.build_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.monitor_permissions)

    def build_ui(self):
        # Title
        title = QLabel("📱 Active App Permission Monitor")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

        subtitle = QLabel("Detects suspicious permissions in real-time")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #a0a0a0;")
        self.layout.addWidget(subtitle)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["App Name", "Permissions", "Status"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.table)

        # Start Button
        btn_layout = QHBoxLayout()
        self.monitor_button = QPushButton("▶️ Start Real-Time Monitoring")
        self.monitor_button.setFont(QFont("Segoe UI", 12))
        self.monitor_button.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                padding: 10px;
                border-radius: 8px;
                color: white;
            }
            QPushButton:hover {
                background-color: #005999;
            }
        """)
        self.monitor_button.clicked.connect(self.start_monitoring)
        btn_layout.addWidget(self.monitor_button)

        # Description Box
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: #dcdcdc;
                border-radius: 5px;
                padding: 8px;
            }
        """)
        self.layout.addLayout(btn_layout)
        self.layout.addWidget(self.output)

    def start_monitoring(self):
        self.output.append("🛰️ Monitoring started...")
        self.timer.start(3000)
        self.analyze_permissions()

    def monitor_permissions(self):
        processes = self.get_running_processes()
        self.update_table(processes)

    def get_running_processes(self):
        processes_info = []
        for proc in psutil.process_iter(['pid', 'name']):
            proc_name = proc.info['name']
            permissions = self.get_process_permissions(proc_name)
            unwanted = ["Camera", "Microphone", "Contacts", "access_network"]
            status = "⚠️ Unwanted" if any(p in unwanted for p in permissions) else "✅ Safe"
            processes_info.append((proc_name, ', '.join(permissions), status))
        return processes_info

    def get_process_permissions(self, process_name):
        # Simulated permission mapping
        permissions_map = {
            "chrome.exe": ["access_network", "read_files", "write_files"],
            "python.exe": ["access_network", "read_files"],
            "notepad.exe": ["read_files"],
            "CameraApp": ["Camera", "Microphone"],
            "MapsApp": ["Location", "Storage"],
            "NotesApp": ["Storage"],
            "RandomGame": ["Camera", "Contacts", "Location", "Microphone"]
        }
        return permissions_map.get(process_name, [])

    def update_table(self, processes):
        self.table.setRowCount(0)
        for row, (name, perms, status) in enumerate(processes):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(perms))
            status_item = QTableWidgetItem(status)

            if "Unwanted" in status:
                status_item.setBackground(QBrush(QColor("#ff4c4c")))
            else:
                status_item.setBackground(QBrush(QColor("#2e8b57")))

            self.table.setItem(row, 2, status_item)

    def analyze_permissions(self):
        apps = {
            "CameraApp": ["Camera", "Microphone"],
            "NotesApp": ["Storage"],
            "MapsApp": ["Location", "Storage"],
            "RandomGame": ["Camera", "Contacts", "Location", "Microphone"]
        }
        unwanted = ["Camera", "Microphone", "Contacts"]

        def scan():
            for app, perms in apps.items():
                self.output.append(f"\n📦 App: {app}")
                for perm in perms:
                    status = "⚠️ Unwanted" if perm in unwanted else "✅ Safe"
                    self.output.append(f"   • {perm}: {status}")
                time.sleep(1)

        threading.Thread(target=scan, daemon=True).start()

# Entry
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PermissionGUI()
    window.show()
    sys.exit(app.exec_())
