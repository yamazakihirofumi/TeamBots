import requests
import json
import getpass
import socket
import sys

# Paste your Power Automate Webhook URL here
WEBHOOK_URL = "https://default7cf48d453ddb4389a9c1c115526eb5.2e.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/fc670e6278f646718c881230cbea8f7b/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=RhpYGAmj-8x9mAWC3iNG4ylh1zGgx6L7JbUqa7TogFY"


def build_message(extra_message=None):
    username = getpass.getuser()
    hostname = socket.gethostname()
    base = f"[{username} on {hostname}] : Warning server {hostname} is in use."
    if extra_message:
        return f"{base} 📢📢📢 {extra_message}"
    return base


def send_notification(extra_message=None):
    message_text = build_message(extra_message)
    print(f"Sending notification: {message_text}")

    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": None,
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.2",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": message_text,
                            "wrap": True
                        }
                    ]
                }
            }
        ]
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(WEBHOOK_URL, headers=headers, data=json.dumps(payload))
        if response.status_code in [200, 202]:
            print(f"✅ Success! Notification sent to Teams. (Status: {response.status_code})")
        else:
            print(f"❌ Failed to send notification.")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    extra = sys.argv[1] if len(sys.argv) > 1 else None
    send_notification(extra)
