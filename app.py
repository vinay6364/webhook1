import os
from flask import Flask, request

app = Flask(__name__)

# Get sensitive data from environment variables
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Verification request from Meta (only when setting up the webhook)
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        # Verify that the token matches
        if verify_token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Invalid token", 403
    
    elif request.method == "POST":
        # Handling incoming messages
        data = request.get_json()

        if data.get("object") == "whatsapp_business_account":
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    for message in messages:
                        from_number = message["from"]
                        user_message = message.get("text", {}).get("body", "").strip().lower()

                        if user_message == "start":
                            send_whatsapp_message(from_number, "Hi, how are you doing?")

        return "EVENT_RECEIVED", 200

def send_whatsapp_message(to, message):
    """Send a message via WhatsApp Cloud API."""
    import requests

    url = f"https://graph.facebook.com/v14.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": message}
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")

@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

if __name__ == "__main__":
    # Change port to the dynamic one provided by Render
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

