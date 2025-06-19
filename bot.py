import requests
from webhook_payload import TextMessagePayload

# Define responses for specific commands
RESPONSES = {
    'היי אמא': 'תפסיקי לשגע אותי',
}

def send_whapi_request(payload):
    """Send a request to the WhatsApp API."""
    url = "https://gate.whapi.cloud/messages/text"
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer ***"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(f"Response status: {response.status_code}\n")
    print(f"Response headers: {response.headers}\n")
    print(f"Response from API: {response.text}\n")

    if response.status_code != 200:
        error_msg = {
            'status_code': response.status_code,
            'response_text': response.text,
            'requested_url': url,
            'payload': payload
        }
        print("API Error:", error_msg)
        return error_msg
    return response.json()

def process_message(message):
    """Process incoming WhatsApp message and return appropriate response payload."""
    sender_number = message.get('from', '').strip()
    print(f"Message from number: {sender_number}\n")

    # Only process messages from the specific number
    if sender_number != "972546626125":
        print(f"Skipping message from {sender_number} - not the debug number\n")
        return None

    # Ignore messages from the bot itself
    if message.get('fromMe'):
        return None

    command_type = message.get('type', '').strip().lower()
    
    # Create a base payload object for the specific number we're testing with
    base_payload = {
        "to": "972546626125",
    }

    print(f"Received message type: {command_type}\n")
    
    if command_type == 'text':
        # Get the command text from the incoming message
        command_text = message.get('text', {}).get('body', '').strip().lower()
        
        # Determine the response based on the command
        if command_text == 'היי אמא':
            return TextMessagePayload(
                to=base_payload["to"],
                body=RESPONSES['היי אמא']
            ).to_dict()
        else:
            print(f"Unknown command received: {command_text}. No response sent.\n")
            return None

    return None