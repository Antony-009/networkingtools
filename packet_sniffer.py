from scapy.all import sniff
from ids.detection_engine import detect_intrusion

def start_sniffing(callback):
    def process_packet(packet):
        alert = detect_intrusion(packet)
        if alert:
            callback(f"⚠️ Alert: {alert}")
        else:
            callback("Packet OK")

    sniff(prn=process_packet, store=0, count=10)  # count=10 for testing
