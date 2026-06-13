# LinkedIn Announcement — StratoSentry NIDS AWS DevSecOps Migration

Drafts for sharing the project update on LinkedIn, in three languages.

---

## 🇹🇷 Türkçe

🛡️☁️ **StratoSentry NIDS artık AWS üzerinde — DevSecOps yaklaşımıyla baştan kuruldu!**

Geliştirdiğim hafif Python tabanlı Network Intrusion Detection System (NIDS) projesini Azure'dan **AWS**'ye taşıdım ve uçtan uca otomatize edilmiş bir **DevSecOps** mimarisine dönüştürdüm.

Bu sürümde sadece "çalışan bir uygulama" değil, **tek komutla ayağa kalkan, tekrarlanabilir ve güvenli bir altyapı** hedefledim:

🔹 **Infrastructure as Code (Terraform):** VPC, Subnet, Internet Gateway, Security Group, IAM Role & Instance Profile ve EC2 — hepsi kod olarak versiyonlanıyor.

🔹 **Configuration Management (Ansible):** Sunucu sıfırdan otomatik provizyon ediliyor — bağımlılıklar, Python virtualenv ve `systemd` servisi (otomatik restart dahil) tek playbook ile kuruluyor.

🔹 **Cloud-Native Logging (boto3 + CloudWatch):** Tespit edilen tehditler AWS CloudWatch Logs'a akıyor. Kimlik doğrulama **IAM Instance Profile** ile *keyless* — sunucuda hiçbir statik kimlik bilgisi tutulmuyor. 🔐

🔹 **Uçtan uca doğrulama:** Simüle edilen bir port-scan'in, gerçek bir "Port Scanning Detected" alarmı olarak CloudWatch'a ulaştığını teyit ettim. ✅

En büyük çıkarım: Güvenlik, mimarinin **en başına** (least-privilege IAM, keyless auth, IaC ile denetlenebilirlik) gömüldüğünde, "güvenlik aracı"nın kendisinin de güvenli ve tekrarlanabilir şekilde deploy edilmesi mümkün oluyor.

Kod açık kaynak 👇
🔗 github.com/haydarkozat/stratosentry-nids

\#DevSecOps #AWS #Terraform #Ansible #Python #CloudSecurity #IaC #CloudWatch #NIDS #InfrastructureAsCode

---

## 🇬🇧 English

🛡️☁️ **StratoSentry NIDS now runs on AWS — rebuilt from the ground up with a DevSecOps mindset!**

I migrated my lightweight, Python-based Network Intrusion Detection System (NIDS) from Azure to **AWS** and turned it into a fully automated, end-to-end **DevSecOps** architecture.

This release wasn't just about shipping a working app — the goal was **repeatable, secure infrastructure that comes up with a single command**:

🔹 **Infrastructure as Code (Terraform):** VPC, Subnet, Internet Gateway, Security Group, IAM Role & Instance Profile, and EC2 — all version-controlled as code.

🔹 **Configuration Management (Ansible):** The server is provisioned from scratch automatically — dependencies, a Python virtualenv, and a `systemd` service (with auto-restart on failure) are all set up via a single playbook.

🔹 **Cloud-Native Logging (boto3 + CloudWatch):** Detected threats stream straight into AWS CloudWatch Logs. Authentication is *keyless*, handled by an **IAM Instance Profile** — no static credentials ever live on the host. 🔐

🔹 **End-to-end verification:** I confirmed that a simulated port scan surfaces as a real "Port Scanning Detected" alert in CloudWatch. ✅

My biggest takeaway: when security is baked in from the **very start** of the architecture — least-privilege IAM, keyless auth, auditability through IaC — even a *security tool itself* can be deployed in a secure and reproducible way.

The code is open source 👇
🔗 github.com/haydarkozat/stratosentry-nids

\#DevSecOps #AWS #Terraform #Ansible #Python #CloudSecurity #IaC #CloudWatch #NIDS #InfrastructureAsCode

---

## 🇩🇪 Deutsch

🛡️☁️ **StratoSentry NIDS läuft jetzt auf AWS — von Grund auf mit einem DevSecOps-Ansatz neu aufgebaut!**

Ich habe mein leichtgewichtiges, Python-basiertes Network Intrusion Detection System (NIDS) von Azure zu **AWS** migriert und in eine vollständig automatisierte, durchgängige **DevSecOps**-Architektur überführt.

Bei diesem Release ging es nicht nur um eine lauffähige Anwendung — das Ziel war eine **reproduzierbare, sichere Infrastruktur, die per einzigem Befehl hochfährt**:

🔹 **Infrastructure as Code (Terraform):** VPC, Subnetz, Internet Gateway, Security Group, IAM-Rolle & Instanzprofil sowie EC2 — alles als Code versioniert.

🔹 **Configuration Management (Ansible):** Der Server wird vollständig automatisch bereitgestellt — Abhängigkeiten, eine Python-virtualenv und ein `systemd`-Dienst (inkl. automatischem Neustart bei Fehlern) werden über ein einziges Playbook eingerichtet.

🔹 **Cloud-Native Logging (boto3 + CloudWatch):** Erkannte Bedrohungen fließen direkt in AWS CloudWatch Logs. Die Authentifizierung erfolgt *schlüssellos* über ein **IAM-Instanzprofil** — auf dem Host liegen zu keinem Zeitpunkt statische Zugangsdaten. 🔐

🔹 **Durchgängige Verifizierung:** Ich habe bestätigt, dass ein simulierter Portscan als echte „Port Scanning Detected"-Warnung in CloudWatch erscheint. ✅

Meine wichtigste Erkenntnis: Wenn Sicherheit von **Anfang an** in die Architektur eingebaut wird — Least-Privilege-IAM, schlüssellose Authentifizierung, Nachvollziehbarkeit durch IaC — lässt sich sogar ein *Sicherheitstool selbst* sicher und reproduzierbar ausrollen.

Der Code ist Open Source 👇
🔗 github.com/haydarkozat/stratosentry-nids

\#DevSecOps #AWS #Terraform #Ansible #Python #CloudSecurity #IaC #CloudWatch #NIDS #InfrastructureAsCode
