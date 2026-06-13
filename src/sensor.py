import time
from scapy.all import sniff, IP, TCP
from cloudwatch_logger import CloudWatchLogger

class StratoSentrySensor:
    def __init__(self, interface, cloud_logger=None):
        self.interface = interface
        self.cloud_logger = cloud_logger
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
        if self.cloud_logger:
            if self.cloud_logger.send_alert(alert):
                print("[+] Tehdit verisi başarıyla AWS CloudWatch Logs'a aktarıldı.")
            else:
                print("[-] Bulut entegrasyon kaydı başarısız oldu.")
        else:
             print("[-] CloudWatch Logger yapılandırılmadı, sadece yerel log alındı.")

    def start_sniffing(self):
        print(f"[*] StratoSentry Ağ Sensörü Aktif. Dinlenen Arayüz: {self.interface}...")
        sniff(iface=self.interface, prn=self.analyze_packet, store=False)

if __name__ == "__main__":
    # CloudWatch ayarları (bölge EC2 üzerinde instance profile'dan otomatik alınır)
    LOG_GROUP = "StratoSentryAlerts"
    LOG_STREAM = "sensor-alerts"
    REGION = "eu-central-1"

    # cloud_logger = CloudWatchLogger(log_group=LOG_GROUP, log_stream=LOG_STREAM, region=REGION)

    # Wi-Fi arayüzü genellikle en0 olur
    sensor = StratoSentrySensor(interface="lo0", cloud_logger=None)
    sensor.start_sniffing()
