# StratoSentry NIDS 🛡️☁️

**Cloud-Integrated Network Intrusion Detection System**

StratoSentry is a lightweight, highly efficient Python-based Network Intrusion Detection System (NIDS). It is designed to monitor local network interfaces for malicious activities, such as heuristic port scans, and seamlessly stream security events directly to a Microsoft Azure Log Analytics Workspace via secure REST APIs.

## 🚀 Features
* **Real-time Packet Inspection:** Built on `scapy` for fast and reliable traffic analysis.
* **Heuristic Threat Detection:** Automatically identifies anomalous patterns like SYN floods and aggressive port scanning.
* **Cloud-Native SIEM Integration:** Forwards localized threat data to Microsoft Azure for centralized monitoring and alerting.
* **Lightweight Architecture:** Minimal resource footprint, suitable for edge devices or local gateways.

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **Core Libraries:** Scapy, Requests, Hashlib, HMAC
* **Cloud Provider:** Microsoft Azure (Log Analytics Workspace API)

## ⚙️ Quick Start
1. Clone the repository: `git clone https://github.com/YOUR_USERNAME/stratosentry-nids.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your Azure Workspace ID and Shared Key in the environment variables.
4. Run the sensor (requires root/admin privileges): `sudo python3 src/sensor.py`

---
*Developed with a focus on modern hybrid-cloud security architectures.*