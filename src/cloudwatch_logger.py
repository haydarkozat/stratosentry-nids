import json
import time

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class CloudWatchLogger:
    """Streams StratoSentry alerts to AWS CloudWatch Logs.

    Authentication uses the default boto3 credential chain, so on an EC2
    instance with the StratoSentry IAM instance profile attached no static
    keys are required. Locally it falls back to environment variables,
    shared credentials, or an assumed role as usual.
    """

    def __init__(self, log_group="StratoSentryAlerts", log_stream="sensor-alerts", region=None):
        self.log_group = log_group
        self.log_stream = log_stream
        self.client = boto3.client("logs", region_name=region)
        self._ensure_log_target()

    def _ensure_log_target(self):
        """Create the log group and stream if they do not already exist."""
        try:
            self.client.create_log_group(logGroupName=self.log_group)
        except ClientError as e:
            if e.response["Error"]["Code"] != "ResourceAlreadyExistsException":
                raise

        try:
            self.client.create_log_stream(
                logGroupName=self.log_group,
                logStreamName=self.log_stream,
            )
        except ClientError as e:
            if e.response["Error"]["Code"] != "ResourceAlreadyExistsException":
                raise

    def send_alert(self, alert_data):
        # CloudWatch expects a Unix timestamp in milliseconds.
        timestamp_ms = int(time.time() * 1000)
        alert_data["timestamp"] = timestamp_ms

        try:
            self.client.put_log_events(
                logGroupName=self.log_group,
                logStreamName=self.log_stream,
                logEvents=[
                    {
                        "timestamp": timestamp_ms,
                        "message": json.dumps(alert_data),
                    }
                ],
            )
            return True
        except (BotoCoreError, ClientError) as e:
            print(f"[-] AWS CloudWatch İletişim Hatası: {e}")
            return False
