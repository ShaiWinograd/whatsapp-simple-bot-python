from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from src.chat import MessageHandler, ConversationManager
from src.utils.whatsapp_client import WhatsAppClient
from src.business.flow_factory import BusinessFlowFactory

load_dotenv()  # Load environment variables from a .env file

# Initialize the message handler with its dependencies
conversation_manager = ConversationManager()
message_handler = MessageHandler(conversation_manager, BusinessFlowFactory())

app = Flask(__name__)

def _validate_webhook_data(data):
    """Validate incoming webhook data and check for status updates.
    Args:
        data (dict): The webhook request data to validate.
    Returns:
        Tuple: (early_response, status_code, messages)
    """
    if data.get('event', {}).get('type') == 'statuses':
        return 'Status update received', 200, None
    
    messages = data.get('messages', [])
    if not messages:
        return 'No messages to process', 200, None
    
    return None, None, messages

def _send_message_responses(payloads):
    """Send message responses and handle any sending errors.
    Args:
        payloads (list): List of payloads to send.
    """
    for payload in payloads:
        WhatsAppClient.send_message(payload)

def _handle_error(e, request_data):
    """Handle and format error responses.
    Args:
        e (Exception): The exception that occurred.
        request_data (dict): The request data that caused the error.
    Returns:
        Tuple: (error_response, status_code)
    """
    error_details = {
        'error': str(e)
    }
    return jsonify(error_details), 500

@app.route('/hook', methods=['POST'])
def handle_new_messages():
    """Main webhook handler for processing new messages.
    Returns:
        Response: JSON response indicating success or failure.
    """
    try:
        data = request.json
        # Validate webhook data
        early_response, status_code, messages = _validate_webhook_data(data)
        if early_response:
            return early_response, status_code
            
        # Process messages and send responses
        for message in messages:
            payloads = message_handler.process_message(message)
            if payloads:
                try:
                    _send_message_responses(payloads)
                except Exception as e:
                    raise

        return jsonify({"status": "success"}), 200
    
    except Exception as e:
        return _handle_error(e, request.json)

@app.route('/', methods=['GET'])
def index():
    return 'Bot is running'

if __name__ == '__main__':
    app.run(port=int(os.getenv('PORT', 5000)), debug=True)