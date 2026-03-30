#!/bin/bash

# Reads the current user and hostname, then sends a Teams notification via webhook.
# Usage:
#   ./notification.sh                         # Base warning message
#   ./notification.sh "additional message"    # Warning + extra message

WEBHOOK_URL="https://default7cf48d453ddb4389a9c1c115526eb5.2e.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/fc670e6278f646718c881230cbea8f7b/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=RhpYGAmj-8x9mAWC3iNG4ylh1zGgx6L7JbUqa7TogFY"

USERNAME=$(whoami)
HOSTNAME=$(hostname)
BASE_MESSAGE="[${USERNAME} on ${HOSTNAME}] : Warning server ${HOSTNAME} is in use."

if [ -n "$1" ]; then
    MESSAGE="${BASE_MESSAGE} 📢📢📢 $1"
else
    MESSAGE="${BASE_MESSAGE}"
fi

echo "Sending notification: ${MESSAGE}"

PAYLOAD=$(cat <<EOF
{
  "type": "message",
  "attachments": [
    {
      "contentType": "application/vnd.microsoft.card.adaptive",
      "contentUrl": null,
      "content": {
        "\$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.2",
        "body": [
          {
            "type": "TextBlock",
            "text": "${MESSAGE}",
            "wrap": true
          }
        ]
      }
    }
  ]
}
EOF
)

HTTP_STATUS=$(curl -s -o /tmp/teams_response.txt -w "%{http_code}" \
    -X POST \
    -H "Content-Type: application/json" \
    -d "${PAYLOAD}" \
    "${WEBHOOK_URL}")

if [ "${HTTP_STATUS}" -eq 200 ] || [ "${HTTP_STATUS}" -eq 202 ]; then
    echo "✅ Success! Notification sent to Teams. (Status: ${HTTP_STATUS})"
else
    echo "❌ Failed to send notification."
    echo "Status Code: ${HTTP_STATUS}"
    echo "Response: $(cat /tmp/teams_response.txt)"
fi
