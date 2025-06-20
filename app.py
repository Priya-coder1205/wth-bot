from flask import Flask, request
import requests

from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Use your actual OpenRouter API key here
OPENROUTER_API_KEY = "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"

def get_chatgpt_response(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/Priya-coder1205",  # Replace with any URL
        "X-Title": "whatsapp-agent"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",  # or any supported one like meta/llama-3
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

@app.route("/", methods=["GET"])
def home():
    return "Shinigami.X is online!"


@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get('Body')
    resp = MessagingResponse()

    if incoming_msg:
        reply = get_chatgpt_response(incoming_msg)
        resp.message(reply)
    else:
        resp.message("Send something!")
    
    return str(resp), 200

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Default to 10000 if PORT not set
    app.run(host="0.0.0.0", port=port, debug=True)

