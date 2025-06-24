"""WhatsApp API client for sending messages and managing labels."""
import requests
from src.config.whatsapp import API as WHATSAPP_API, LABELS as WHATSAPP_LABELS, get_api_url

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
        # Determine message type from payload
        message_type = 'text'
        if 'type' in payload:
            message_type = payload['type']
            # 'button' type should use 'interactive' endpoint
            if message_type == 'button':
                message_type = 'interactive'
            
        api_url = get_api_url(message_type)
        try:
            response = requests.post(
                api_url,
                json=payload,
                headers=WHATSAPP_API['headers']
            )
            
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
            error_msg = {
                'error': f"Error sending request: {str(e)}",
                'requested_url': api_url,
                'payload': payload
            }
            print("Request Error:", error_msg)
            return error_msg

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
            
            print(f"Applied label {label_id} to {phone_number}")
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
            
            print(f"Removed label {label_id} from {phone_number}")
            return response.json()
            
        except Exception as e:
            print(f"Error removing label: {str(e)}\n")
            raise