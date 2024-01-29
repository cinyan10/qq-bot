import requests
import json
from config import WEBHOOK_URL, SERVER_LIST
from functions.steam.a2s import query_server_simple


def send_webhook():
    info_data = ''
    for s in SERVER_LIST:
        info_data += query_server_simple(s)

    payload = {
        "content": "",
        "embeds": [
            {
                "title": "SERVER LIST",
                "description": info_data,
                "color": 0x60FFFF,  # Hex color code, e.g., red
                # "footer": {"text": "Your Footer"},
            }
        ]
    }

    # Send the POST request to the webhook URL with the payload
    headers = {"Content-Type": "application/json"}
    response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers=headers)

    # Print the response from the server
    print(response.text)


if __name__ == "__main__":
    pass
