# StratoSentry NIDS 🛡️☁️

**Cloud-Integrierte Netzwerk-Angriffserkennung**

StratoSentry ist ein leichtgewichtiges, Python-basiertes Network Intrusion Detection System (NIDS). Es überwacht lokale Netzwerkschnittstellen auf verdächtige Aktivitäten (z. B. Portscans) und leitet Sicherheitsereignisse in Echtzeit über sichere REST-APIs direkt an einen Microsoft Azure Log Analytics Workspace weiter.

## 🚀 Hauptmerkmale
* **Paketinspektion in Echtzeit:** Basierend auf `scapy` für eine schnelle und zuverlässige Netzwerkanalyse.
* **Heuristische Bedrohungserkennung:** Identifiziert automatisch Anomalien wie aggressive Portscans.
* **Native Cloud-SIEM-Anbindung:** Leitet lokale Bedrohungsdaten zur zentralen Überwachung an Microsoft Azure weiter.
* **Ressourcenschonende Architektur:** Ideal für Edge-Geräte und lokale Gateways.

## 🛠️ Technologien
* **Sprache:** Python 3.9+
* **Bibliotheken:** Scapy, Requests, Hashlib
* **Cloud-Infrastruktur:** Microsoft Azure (Log Analytics Workspace)

## ⚙️ Schnellstart
1. Repository klonen: `git clone https://github.com/YOUR_USERNAME/stratosentry-nids.git`
2. Abhängigkeiten installieren: `pip install -r requirements.txt`
3. Azure Workspace ID und Shared Key konfigurieren.
4. Sensor starten (Root-Rechte erforderlich): `sudo python3 src/sensor.py`