# StratoSentry NIDS 🛡️☁️

**Cloud-Integrated Network Intrusion Detection System**

StratoSentry is a lightweight, highly efficient Python-based Network Intrusion Detection System (NIDS). It is designed to monitor local network interfaces for malicious activities, such as heuristic port scans, and seamlessly stream security events directly to AWS CloudWatch Logs using the AWS SDK (`boto3`).

## 🚀 Features
* **Real-time Packet Inspection:** Built on `scapy` for fast and reliable traffic analysis.
* **Heuristic Threat Detection:** Automatically identifies anomalous patterns like SYN floods and aggressive port scanning.
* **Cloud-Native SIEM Integration:** Forwards localized threat data to AWS CloudWatch Logs for centralized monitoring and alerting.
* **Keyless Authentication:** On EC2, the sensor authenticates via an IAM instance profile — no static credentials to manage.
* **Infrastructure as Code:** The full AWS environment (VPC, EC2, IAM, security group) is provisioned with Terraform under `infrastructure/`.
* **Lightweight Architecture:** Minimal resource footprint, suitable for edge devices or local gateways.

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **Core Libraries:** Scapy, boto3
* **Cloud Provider:** Amazon Web Services (CloudWatch Logs)
* **Infrastructure:** Terraform (AWS provider)

## ☁️ Provision the Infrastructure
The AWS environment is defined as code in the `infrastructure/` directory:

```bash
cd infrastructure
terraform init
terraform plan
terraform apply
```

This provisions a VPC with a public subnet, a security group (SSH inbound), an EC2 instance (Ubuntu 22.04 LTS) bootstrapped with Python 3, and an IAM role/instance profile granting CloudWatch Logs permissions. Key inputs: `aws_region` (default `eu-central-1`) and `instance_type` (default `t3.micro`).

## ⚙️ Quick Start
1. Clone the repository: `git clone https://github.com/YOUR_USERNAME/stratosentry-nids.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Ensure AWS credentials are available — automatic via the IAM instance profile on EC2, or via `aws configure` / environment variables when running locally.
4. Run the sensor (requires root/admin privileges): `sudo python3 src/sensor.py`

---
*Developed with a focus on modern hybrid-cloud security architectures.*