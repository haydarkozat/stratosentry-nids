import time
from scapy.all import sniff, IP, TCP
from azure_logger import AzureLogAnalyticsLogger

class StratoSentrySensor:
    def __init__(self, interface, azure_logger=None):
        self.interface = interface
        self.azure_logger = azure_logger
        self.ip_track = {}
        self.SCAN_THRESHOLD = 20  # 10 saniye içinde farklı port isteği eşiği

    def analyze_packet(self, packet):
        if not packet.haslayer(IP) or not packet.haslayer(TCP):
            return

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        dst_port = packet[TCP].dport
        current_time = time.time()

        if src_ip not in self.ip_track:
            self.ip_track[src_ip] = {"ports": set(), "start_time": current_time}
        
        # 10 saniyelik zaman penceresini kontrol et
        if current_time - self.ip_track[src_ip]["start_time"] > 10:
            self.ip_track[src_ip] = {"ports": set(), "start_time": current_time}
        
        self.ip_track[src_ip]["ports"].add(dst_port)
        
        # Eşik değeri aşılırsa uyarı tetikle
        if len(self.ip_track[src_ip]["ports"]) > self.SCAN_THRESHOLD:
            alert = {
                "AlertType": "Port Scanning Detected",
                "Severity": "High",
                "AttackerIP": src_ip,
                "TargetIP": dst_ip,
                "Details": f"Attacker scanned {len(self.ip_track[src_ip]['ports'])} unique ports within 10s."
            }
            self.trigger_alert(alert)
            self.ip_track[src_ip]["ports"] = set() # Uyarının tekrarlamaması için sıfırla

    def trigger_alert(self, alert):
        print(f"[!] TEHDİT TESPİT EDİLDİ: {alert['AlertType']} | Saldırgan: {alert['AttackerIP']}")
        if self.azure_logger:
            if self.azure_logger.send_alert(alert):
                print("[+] Tehdit verisi başarıyla Azure Log Analytics'e aktarıldı.")
            else:
                print("[-] Bulut entegrasyon kaydı başarısız oldu.")
        else:
             print("[-] Azure Logger yapılandırılmadı, sadece yerel log alındı.")

    def start_sniffing(self):
        print(f"[*] StratoSentry Ağ Sensörü Aktif. Dinlenen Arayüz: {self.interface}...")
        sniff(iface=self.interface, prn=self.analyze_packet, store=False)

if __name__ == "__main__":
    # Test için dummy workspace id'ler (Gerçek senaryoda .env dosyasından çekilecektir)
    WORKSPACE_ID = "DEMO_WORKSPACE_ID"
    SHARED_KEY = "DEMO_SHARED_KEY"
    
    # azure_logger = AzureLogAnalyticsLogger(workspace_id=WORKSPACE_ID, shared_key=SHARED_KEY)
    
    # Wi-Fi arayüzü genellikle en0 olur
    sensor = StratoSentrySensor(interface="en0", azure_logger=None)
    sensor.start_sniffing()
