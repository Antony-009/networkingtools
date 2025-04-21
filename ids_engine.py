import threading
import time
from scapy.all import sniff

def process_packet(packet, output):
    info = f"Packet: {packet.summary()}"
    output.append(info)

def start_ids_analysis(output_widget):
    def sniff_packets():
        sniff(prn=lambda pkt: process_packet(pkt, output_widget), store=0)

    thread = threading.Thread(target=sniff_packets, daemon=True)
    thread.start()
