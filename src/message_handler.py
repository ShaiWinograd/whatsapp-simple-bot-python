"""Core message processing logic for WhatsApp bot."""
from typing import List, Dict, Any
from venv import logger

from src.config.responses import RESPONSES, DEBUG_PHONE_NUMBER
from src.conversation_manager import ConversationManager
from src.services.service_factory import ServiceFactory, ServiceType
from src.utils.errors import ConversationError
from src.utils.validators import validate_sender
from src.services import create_service
from webhook_payload import TextMessagePayload, InteractiveMessagePayload


class MessageHandler:
    def __init__(self, conversation_manager: ConversationManager, service_factory: ServiceFactory):
        self.conversation_manager = conversation_manager
        self.service_factory = service_factory

    def handle_interactive_message(self, message: Dict[str, Any], base_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Handle interactive message type and return appropriate response.
        Args:
            message (dict): The incoming WhatsApp message
            base_payload (dict): Base payload for response message
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        button_reply = message.get('interactive', {}).get('button_reply', {})
        selected_option = button_reply.get('id', '')
        recipient = base_payload["to"]

        # Check existing conversation
        service = self.conversation_manager.get_conversation(recipient)
        if service:
            return service.handle_response(message)

        # Create new conversation if service selection
        if selected_option in RESPONSES['options']:
            try:
                service_type = ServiceType(selected_option)
                service = self.service_factory.create(service_type, recipient)
                self.conversation_manager.add_conversation(recipient, service)
                return service.handle_initial_message()
            except (ValueError, ConversationError) as e:
                logger.error(f"Failed to create service: {e}")
                return self.create_welcome_messages(recipient)

        return self.create_welcome_messages(recipient)
    

    def handle_text_message(self, message: Dict[str, Any], base_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Handle text message type and return appropriate response.
        
        Args:
            message (dict): The incoming WhatsApp message
            base_payload (dict): Base payload for response message
            
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        recipient = base_payload["to"]

        # Check existing conversation
        service = self.conversation_manager.get_conversation(recipient)
        if service:
            return service.handle_response(message)

        # For any other text message, show the welcome message
        return self.create_welcome_messages(recipient)
    

    def create_welcome_messages(self, recipient: str) -> List[Dict[str, Any]]:
        """
        Create welcome and options messages.
        
        Args:
            recipient (str): The recipient's phone number
            
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        # Create interactive options message
        options_message = InteractiveMessagePayload(
            to=recipient,
            body=RESPONSES['welcome_message'],
            button_messages=RESPONSES['options']
        ).to_dict()
        
        return [options_message]
    

    def process_message(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process incoming WhatsApp message and return appropriate response payload.
        
        Args:
            message (dict): The incoming WhatsApp message
            
        Returns:
            List[Dict[str, Any]]: List of message payloads to send or empty list if no response needed
        """
        if not validate_sender(message):
            return []

        sender_number = message.get('from', '').strip()
        
        # Only process messages from the debug phone number
        if sender_number != DEBUG_PHONE_NUMBER:
            return []

        # Create a base payload object with the sender's number
        base_payload = {
            "to": sender_number,
        }

        command_type = message.get('type', '').strip().lower()
        print(f"Received message type: {command_type}\n")
        
        if command_type == 'text':
            return self.handle_text_message(message, base_payload)
        elif command_type in ['interactive', 'reply']:
            # For reply type, check if it's a button reply
            if command_type == 'reply' and message.get('reply', {}).get('type') == 'buttons_reply':
                # Extract the actual title from the button reply
                button_title = message.get('reply', {}).get('buttons_reply', {}).get('title', '')
                print(f"Received button reply with title: {button_title}")
                
                if button_title in RESPONSES['options']:
                    print(f"Creating service for option: {button_title}")
                    service = create_service(button_title, base_payload["to"])
                    if service:
                        print(f"Service created successfully")
                        self.conversation_manager.add_conversation(base_payload["to"], service)
                        return service.handle_initial_message()
                    else:
                        print(f"Failed to create service for option: {button_title}")
                else:
                    print(f"Button title not found in RESPONSES options: {button_title}")
                    
            return self.handle_interactive_message(message, base_payload)

        print(f"Unhandled message type: {command_type}")
        return []
    