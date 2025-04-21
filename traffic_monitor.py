import psutil
import time
from PyQt5.QtCore import QThread, pyqtSignal

class TrafficMonitor(QThread):
    traffic_data = pyqtSignal(float, float)

    def run(self):
        prev_sent = psutil.net_io_counters().bytes_sent
        prev_recv = psutil.net_io_counters().bytes_recv

        while True:
            time.sleep(1)
            curr_sent = psutil.net_io_counters().bytes_sent
            curr_recv = psutil.net_io_counters().bytes_recv

            upload = (curr_sent - prev_sent) / 1024
            download = (curr_recv - prev_recv) / 1024

            prev_sent = curr_sent
            prev_recv = curr_recv

            self.traffic_data.emit(upload, download)
