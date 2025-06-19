from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from src.message_handler import process_message
from src.utils.whatsapp_client import WhatsAppClient

load_dotenv()  # Load environment variables from a .env file

app = Flask(__name__)

# The Webhook link to your server is set in the dashboard. For this script it is important that the link is in the format: {link to server}/hook.
@app.route('/hook', methods=['POST'])
def handle_new_messages():
    try:
        # Log incoming webhook data
        print("Received webhook data:", request.json)
        
        # Check if this is a status update
        if request.json.get('event', {}).get('type') == 'statuses':
            return 'Status update received', 200
            
        messages = request.json.get('messages', [])
        if not messages:
            return 'No messages to process', 200
            
        for message in messages:
            # Process the message and get response payload
            payloads = process_message(message)
            if payloads:
                try:
                    # Send each response in the list
                    for payload in payloads:
                        print(f"Full payload: {payload}\n")  # Log complete payload
                        response = WhatsAppClient.send_message(payload)
                        print(f"API Response: {response}\n")
                except Exception as e:
                    print(f"Error sending message: {str(e)}\n")
                    raise

        return jsonify({"status": "success"}), 200
    
    except Exception as e:
        error_details = {
            'error': str(e),
            'message_data': request.json
        }
        print(f"Error details: {error_details}\n")
        return jsonify(error_details), 500

@app.route('/', methods=['GET'])
def index():
    return 'Bot is running'

if __name__ == '__main__':
    app.run(port=int(os.getenv('PORT', 5000)), debug=True)