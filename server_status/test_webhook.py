import requests
import json

# 1. Paste your newly generated Power Automate Webhook URL here
WEBHOOK_URL = "https://default7cf48d453ddb4389a9c1c115526eb5.2e.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/fc670e6278f646718c881230cbea8f7b/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=RhpYGAmj-8x9mAWC3iNG4ylh1zGgx6L7JbUqa7TogFY"

# 2. Construct the Adaptive Card JSON payload
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
                        "text": "🧪 **Test: Message Status by webhook**",
                        "weight": "bolder",
                        "size": "medium",
                        "color": "accent"
                    },
                    {
                        "type": "TextBlock",
                        "text": "This is the test for the message body and it will be replaced by some real text about jobs status here later",
                        "wrap": True
                    }
                ]
            }
        }
    ]
}

def send_teams_notification():
    print("Sending POST request to Teams...")
    headers = {'Content-Type': 'application/json'}
    
    try:
        # 3. Send the POST request
        response = requests.post(WEBHOOK_URL, headers=headers, data=json.dumps(payload))
        
        # Power Automate webhooks usually return 202 (Accepted) or 200 (OK)
        if response.status_code in [200, 202]:
            print(f"✅ Success! Notification sent to Teams. (Status: {response.status_code})")
        else:
            print(f"❌ Failed to send notification.")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    send_teams_notification()