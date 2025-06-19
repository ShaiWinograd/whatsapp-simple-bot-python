"""WhatsApp API client for sending messages."""
import requests
from src.config.responses import WHATSAPP_API

def send_whapi_request(payload):
    """
    Send a request to the WhatsApp API.
    
    Args:
        payload (dict): The message payload to send
        
    Returns:
        dict: The API response or error details
    """
    response = requests.post(
        WHATSAPP_API['url'], 
        json=payload, 
        headers=WHATSAPP_API['headers']
    )
    
    print(f"Response status: {response.status_code}\n")
    print(f"Response headers: {response.headers}\n")
    print(f"Response from API: {response.text}\n")

    if response.status_code != 200:
        error_msg = {
            'status_code': response.status_code,
            'response_text': response.text,
            'requested_url': WHATSAPP_API['url'],
            'payload': payload
        }
        print("API Error:", error_msg)
        return error_msg
        
    return response.json()