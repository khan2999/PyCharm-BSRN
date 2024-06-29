from scapy.all import sniff
from datetime import datetime

def packet_handler(packet):
    # Erstellen einer menschenlesbaren Darstellung der Protokolldaten
    readable_data = bytes(packet).hex()  # Wandelt das Paket in eine hexadezimale Zeichenfolge um
    with open("network_log.txt", "a") as logfile:  # Öffnet die Logdatei im Anhang-Modus
        logfile.write(f"{datetime.now()}: {readable_data}\n")  # Schreibt die aktuelle Zeit und die Daten in die Logdatei

def start_sniffer():
    print("Sniffer wird gestartet...")
    # Startet den Sniffer und filtert nur TCP-Pakete
    sniff(filter="tcp", prn=packet_handler, store=0)

if __name__ == '__main__':
    start_sniffer()  # Startet den Sniffer, wenn das Skript direkt ausgeführt wird
