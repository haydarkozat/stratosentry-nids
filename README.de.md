# StratoSentry NIDS 🛡️☁️

**Cloud-Integrierte Netzwerk-Angriffserkennung**

StratoSentry ist ein leichtgewichtiges, Python-basiertes Network Intrusion Detection System (NIDS). Es überwacht lokale Netzwerkschnittstellen auf verdächtige Aktivitäten (z. B. Portscans) und leitet Sicherheitsereignisse in Echtzeit über das AWS SDK (`boto3`) direkt an AWS CloudWatch Logs weiter.

## 🚀 Hauptmerkmale
* **Paketinspektion in Echtzeit:** Basierend auf `scapy` für eine schnelle und zuverlässige Netzwerkanalyse.
* **Heuristische Bedrohungserkennung:** Identifiziert automatisch Anomalien wie aggressive Portscans.
* **Native Cloud-SIEM-Anbindung:** Leitet lokale Bedrohungsdaten zur zentralen Überwachung an AWS CloudWatch Logs weiter.
* **Schlüssellose Authentifizierung:** Auf EC2 authentifiziert sich der Sensor über ein IAM-Instanzprofil — keine statischen Zugangsdaten erforderlich.
* **Infrastructure as Code:** Die gesamte AWS-Umgebung (VPC, EC2, IAM, Security Group) wird per Terraform unter `infrastructure/` bereitgestellt.
* **Ressourcenschonende Architektur:** Ideal für Edge-Geräte und lokale Gateways.

## 🛠️ Technologien
* **Sprache:** Python 3.9+
* **Bibliotheken:** Scapy, boto3
* **Cloud-Infrastruktur:** Amazon Web Services (CloudWatch Logs)
* **Infrastruktur:** Terraform (AWS Provider)

## ☁️ Infrastruktur bereitstellen
Die AWS-Umgebung ist als Code im Verzeichnis `infrastructure/` definiert:

```bash
cd infrastructure
terraform init
terraform plan
terraform apply
```

Damit werden eine VPC mit öffentlichem Subnetz, eine Security Group (SSH eingehend), eine EC2-Instanz (Ubuntu 22.04 LTS) mit vorinstalliertem Python 3 sowie eine IAM-Rolle/-Instanzprofil mit CloudWatch-Logs-Berechtigungen erstellt. Wichtige Eingaben: `aws_region` (Standard `eu-central-1`) und `instance_type` (Standard `t3.micro`).

## ⚙️ Schnellstart
1. Repository klonen: `git clone https://github.com/YOUR_USERNAME/stratosentry-nids.git`
2. Abhängigkeiten installieren: `pip install -r requirements.txt`
3. AWS-Zugangsdaten bereitstellen — automatisch über das IAM-Instanzprofil auf EC2 oder lokal via `aws configure` / Umgebungsvariablen.
4. Sensor starten (Root-Rechte erforderlich): `sudo python3 src/sensor.py`