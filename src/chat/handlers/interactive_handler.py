"""Interactive message handler implementation."""
from typing import Dict, Any, List
from venv import logger
from .base_handler import BaseMessageHandler
from ...config.responses import RESPONSES
from ...services.service_factory import ServiceType
from ...utils.errors import ConversationError

# Mapping between Hebrew button titles and ServiceType enum values
SERVICE_TYPE_MAPPING = {
    'מעבר דירה': ServiceType.MOVING,
    'סידור וארגון': ServiceType.ORGANIZATION,
    'אשמח לדבר עם נציג/ה': ServiceType.HUMAN_SUPPORT
}


class InteractiveMessageHandler(BaseMessageHandler):
    """Handler for interactive messages and button replies."""

    def handle_button_reply(self, button_title: str, recipient: str) -> List[Dict[str, Any]]:
        """
        Handle a button reply message.

        Args:
            button_title (str): The title of the button that was clicked
            recipient (str): The recipient's phone number

        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        if button_title not in RESPONSES['options']:
            return self.create_welcome_messages(recipient)

        try:
            service_type = SERVICE_TYPE_MAPPING.get(button_title)
            if service_type is None:
                return self.create_welcome_messages(recipient)
                
            service = self.service_factory.create(service_type, recipient)
            self.conversation_manager.add_conversation(recipient, service)
            return service.handle_initial_message()
        except ConversationError:
            return self.create_welcome_messages(recipient)

    def handle(self, message: Dict[str, Any], base_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Handle interactive message type and return appropriate response.

        Args:
            message (Dict[str, Any]): The incoming WhatsApp message
            base_payload (Dict[str, Any]): Base payload for response message

        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        recipient = base_payload["to"]

        # Get button selection if present
        selected_option = None
        if 'interactive' in message:
            button_reply = message.get('interactive', {}).get('button_reply', {})
            selected_option = button_reply.get('title', '')
        elif 'reply' in message and message.get('reply', {}).get('type') == 'buttons_reply':
            selected_option = message.get('reply', {}).get('buttons_reply', {}).get('title', '')

        # Check if user wants to return to main menu
        if selected_option == 'חזרה לתפריט הראשי':
            self.conversation_manager.remove_conversation(recipient)
            return self.create_welcome_messages(recipient)

        # Check if user wants to switch to human support from any service
        if selected_option == 'אשמח לדבר עם נציג/ה':
            service = self.service_factory.create(ServiceType.HUMAN_SUPPORT, recipient)
            self.conversation_manager.add_conversation(recipient, service)
            return service.handle_initial_message()

        # Check for existing conversation if not returning to main menu or switching to human support
        conversation_response = self.check_existing_conversation(recipient, message)
        if conversation_response is not None:
            return conversation_response

        # Handle regular interactive message
        if 'interactive' in message:
            button_reply = message.get('interactive', {}).get('button_reply', {})
            selected_option = button_reply.get('title', '')  # Use title instead of id
            
            if selected_option in SERVICE_TYPE_MAPPING:
                try:
                    service_type = SERVICE_TYPE_MAPPING[selected_option]
                    service = self.service_factory.create(service_type, recipient)
                    self.conversation_manager.add_conversation(recipient, service)
                    return service.handle_initial_message()
                except ConversationError:
                    return self.create_welcome_messages(recipient)

        # Handle button reply
        elif 'reply' in message and message.get('reply', {}).get('type') == 'buttons_reply':
            button_title = message.get('reply', {}).get('buttons_reply', {}).get('title', '')
            return self.handle_button_reply(button_title, recipient)

        return self.create_welcome_messages(recipient)