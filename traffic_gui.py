# traffic/traffic_gui.py

import sys
import psutil
import time
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class TrafficGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📶 Real-Time Network Traffic Monitor")
        self.setGeometry(150, 150, 800, 500)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Title label
        self.title_label = QLabel("📊 Real-Time Network Traffic")
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Matplotlib graph setup
        self.figure = Figure(facecolor="#2e2e2e")
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor("#2e2e2e")
        self.ax.tick_params(colors='white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.set_xlabel("Time (s)", color='white')
        self.ax.set_ylabel("KB/s", color='white')
        self.layout.addWidget(self.canvas)

        # Data initialization
        self.upload_data = []
        self.download_data = []
        self.time_stamps = []
        self.last_sent = psutil.net_io_counters().bytes_sent
        self.last_recv = psutil.net_io_counters().bytes_recv
        self.counter = 0

        # Start timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)

    def update_plot(self):
        current_sent = psutil.net_io_counters().bytes_sent
        current_recv = psutil.net_io_counters().bytes_recv

        upload_speed = (current_sent - self.last_sent) / 1024.0  # in KB/s
        download_speed = (current_recv - self.last_recv) / 1024.0  # in KB/s

        self.upload_data.append(upload_speed)
        self.download_data.append(download_speed)
        self.time_stamps.append(self.counter)

        self.last_sent = current_sent
        self.last_recv = current_recv
        self.counter += 1

        # Keep only last 60 seconds of data
        self.upload_data = self.upload_data[-60:]
        self.download_data = self.download_data[-60:]
        self.time_stamps = self.time_stamps[-60:]

        self.ax.clear()
        self.ax.plot(self.time_stamps, self.upload_data, label="Upload", color="orange")
        self.ax.plot(self.time_stamps, self.download_data, label="Download", color="cyan")
        self.ax.set_facecolor("#2e2e2e")
        self.ax.set_xlabel("Time (s)", color='white')
        self.ax.set_ylabel("KB/s", color='white')
        self.ax.legend(loc="upper left", facecolor="#2e2e2e", edgecolor="white", labelcolor="white")
        self.ax.tick_params(colors='white')
        self.ax.set_xlim(max(0, self.counter - 60), self.counter)
        self.ax.set_ylim(0, max(self.upload_data + self.download_data + [1]) * 1.5)

        self.canvas.draw()


# Optional: Run standalone
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TrafficGUI()
    win.show()
    sys.exit(app.exec_())
