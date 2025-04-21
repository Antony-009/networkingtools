def detect_intrusion(packet):
    if packet.haslayer("TCP") and packet["TCP"].dport == 23:
        return "Suspicious Telnet traffic detected"
    return None
