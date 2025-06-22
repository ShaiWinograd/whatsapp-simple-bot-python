"""WhatsApp API client for sending messages and managing labels."""
import requests
from src.config.responses import WHATSAPP_API, WHATSAPP_LABELS, get_api_url

class WhatsAppClient:
    """Client for interacting with WhatsApp API."""
    
    @staticmethod
    def send_message(payload: dict) -> dict:
        """
        Send a message via WhatsApp API.
        
        Args:
            payload (dict): The message payload to send
            
        Returns:
            dict: The API response or error details
        """
        # Determine message type from payload structure
        message_type = 'text'
        if 'action' in payload:  # Interactive messages have an action field
            message_type = 'interactive'
            
        api_url = get_api_url(message_type)
        print(f"Sending {message_type} message to URL: {api_url}\n")
        print(f"Payload: {payload}\n")
        
        try:
            response = requests.post(
                api_url,
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
                    'requested_url': api_url,
                    'payload': payload
                }
                print("API Error:", error_msg)
                return error_msg
                
            return response.json()
            
        except Exception as e:
            print(f"Error sending request: {str(e)}\n")
            raise

    @staticmethod
    def apply_label(phone_number: str, label_id: str) -> dict:
        """
        Apply a label to a WhatsApp chat.
        
        Args:
            phone_number (str): The phone number of the chat
            label_id (str): The ID of the label to apply
            
        Returns:
            dict: The API response
        """
        formatted_number = f"{phone_number}@s.whatsapp.net"
        api_url = f"{WHATSAPP_API['base_url']}labels/{label_id}//{formatted_number}"
        
        try:
            response = requests.post(
                api_url,
                headers=WHATSAPP_API['headers']
            )
            
            print(f"Applied label {label_id} to {phone_number}. Response:", response.text)
            return response.json()
            
        except Exception as e:
            print(f"Error applying label: {str(e)}\n")
            raise

    @staticmethod
    def remove_label(phone_number: str, label_id: str) -> dict:
        """
        Remove a label from a WhatsApp chat.
        
        Args:
            phone_number (str): The phone number of the chat
            label_id (str): The ID of the label to remove
            
        Returns:
            dict: The API response
        """
        formatted_number = f"{phone_number}@s.whatsapp.net"
        api_url = f"{WHATSAPP_API['base_url']}labels/{label_id}//{formatted_number}"
        
        try:
            response = requests.delete(
                api_url,
                headers=WHATSAPP_API['headers']
            )
            
            print(f"Removed label {label_id} from {phone_number}. Response:", response.text)
            return response.json()
            
        except Exception as e:
            print(f"Error removing label: {str(e)}\n")
            raise