import json
import requests
import datetime
import hashlib
import hmac
import base64

class AzureLogAnalyticsLogger:
    def __init__(self, workspace_id, shared_key, log_type="StratoSentryAlerts"):
        self.workspace_id = workspace_id
        self.shared_key = shared_key
        self.log_type = log_type

    def _build_signature(self, date, content_length, method, content_type, resource):
        x_headers = 'x-ms-date:' + date
        string_to_hash = f"{method}\n{content_length}\n{content_type}\n{x_headers}\n{resource}"
        bytes_to_hash = bytes(string_to_hash, encoding="utf-8")  
        decoded_key = base64.b64decode(self.shared_key)
        encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, hashlib.sha256).digest()).decode()
        return f"SharedKey {self.workspace_id}:{encoded_hash}"

    def send_alert(self, alert_data):
        alert_data['timestamp'] = datetime.datetime.utcnow().isoformat() + "Z"
        body = json.dumps(alert_data)
        method = 'POST'
        content_type = 'application/json'
        resource = '/api/logs'
        rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        content_length = len(body)
        
        signature = self._build_signature(rfc1123date, content_length, method, content_type, resource)
        uri = f"https://{self.workspace_id}.ods.opinsights.azure.com{resource}?api-version=2016-04-01"
        
        headers = {
            'content-type': content_type,
            'Authorization': signature,
            'Log-Type': self.log_type,
            'x-ms-date': rfc1123date
        }
        
        try:
            response = requests.post(uri, data=body, headers=headers)
            return response.status_code == 200
        except Exception as e:
            print(f"[-] Azure Bulut İletişim Hatası: {e}")
            return False
