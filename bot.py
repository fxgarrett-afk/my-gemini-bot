import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

app = Flask(__name__)

# --- CONFIGURATION ---
# We get the key from the environment variable (Render)
api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # Using the Flash model which is faster
    model = genai.GenerativeModel('gemini-3-flash-preview')

# --- THE ROUTES ---

@app.route("/")
def home():
    return "Hello! The Gemini WhatsApp Bot is running."

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip()
    
    resp = MessagingResponse()
    msg = resp.message()

    if not incoming_msg:
        msg.body("I didn't receive any text!")
        return str(resp)

    try:
        # Check if the key was actually found
        if not api_key:
            msg.body("Error: API Key missing in server settings.")
            return str(resp)

        response = model.generate_content(incoming_msg)
        msg.body(response.text)
        
    except Exception as e:
        msg.body("Sorry, I encountered an error.")
        print(f"Error: {e}")

    return str(resp)

if __name__ == "__main__":
    # This line is for running locally
    app.run(host='0.0.0.0', port=10000)
    