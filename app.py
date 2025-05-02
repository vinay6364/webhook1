from flask import Flask, request, jsonify,session

app = Flask(__name__)

# Replace with your WhatsApp Cloud API credentials
ACCESS_TOKEN = "EAAHZCkHIIBWUBOzhZArR0r0btGENcD6zcAHHfhKhslJ7aNbHfAytPUkgpB14OrEq9iwHOCThZCMVOEpxBlZC3L9GIlnXeF06kJ5ljZBPyOpU6sY0Dc87mugFczyZBXyt9gcngybRQXiiPk7uNXkSzXmATGevkmdCsjwUN4kl5VO6Nz7WHZA0AhKQWuA3tVaUV47rrxTV131CZAq5unj2wCI7wR9oAPqZCruUEvSSMGxti"
PHONE_NUMBER_ID = "553295497877094"


@app.route("/webhook", methods=["POST"])
@app.route("/webhook", methods=["POST"])
def webhook():
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
                        user_name=send_whatsapp_message(from_number,"Whats your name")
                        session['user_name']=user_name

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


if __name__ == "__main__":
    app.run(debug=True, port=5000)
