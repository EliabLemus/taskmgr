import os
import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class SlackAlerter:
    """Send alerts to Slack webhook"""

    def __init__(self):
        self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        self.enabled = bool(self.webhook_url and self.webhook_url.strip())

    def send_alert(
        self, severity, alert_type, message, metric_value=None, threshold=None
    ):
        """
        Send formatted alert to Slack

        Args:
            severity: INFO, WARNING, ERROR, CRITICAL
            alert_type: Type of alert (e.g., 'high_error_rate')
            message: Human-readable message
            metric_value: Current metric value
            threshold: Threshold value that was exceeded
        """
        if not self.enabled:
            logger.warning(f"Slack alerts disabled: {alert_type} - {message}")
            return False

        # Color coding
        colors = {
            "INFO": "#36a64f",  # Green
            "WARNING": "#ff9900",  # Orange
            "ERROR": "#ff0000",  # Red
            "CRITICAL": "#990000",  # Dark Red
        }

        # Build Slack message
        fields = [
            {"title": "Severity", "value": severity, "short": True},
            {"title": "Alert Type", "value": alert_type, "short": True},
        ]

        if metric_value is not None:
            fields.append(
                {
                    "title": "Current Value",
                    "value": f"{metric_value:.2f}",
                    "short": True,
                }
            )

        if threshold is not None:
            fields.append(
                {"title": "Threshold", "value": f"{threshold:.2f}", "short": True}
            )

        payload = {
            "attachments": [
                {
                    "fallback": f"{severity}: {message}",
                    "color": colors.get(severity, "#cccccc"),
                    "title": f"🚨 Task Manager Alert - {severity}",
                    "text": message,
                    "fields": fields,
                    "footer": "Task Manager Monitoring",
                    "ts": int(datetime.utcnow().timestamp()),
                }
            ]
        }

        try:
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info(f"Slack alert sent: {alert_type}")
            return True
        except Exception as e:
            logger.error(f"Failed to send Slack alert: {e}")
            return False


# Singleton instance
slack_alerter = SlackAlerter()
